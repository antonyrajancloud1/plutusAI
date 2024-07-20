from plutusAI.server.base import *
from plutusAI.server.broker.AngelOneBroker import AngelOneBroker


class Scalper:
    def __init__(self, user_email, index, index_group):
        self.initialize_attributes()
        self.user_email = user_email
        self.index_name = index
        self.index_group = index_group

        try:
            self.load_user_data()
            self.initialize_broker()
            self.initialize_scalper()
        except Exception as e:
            addLogDetails(ERROR, f"Initialization error: {str(e)}")

    def initialize_attributes(self):
        self.optionDetails = None
        self.currentOptionPrice = None
        self.started_time = None
        self.exchange = NFO
        self.base_value = None
        self.to_time = None
        self.tf = 1
        self.isCEOrderPlaced = False
        self.isPEOrderPlaced = False
        self.currentPremiumPlaced = None
        self.total_price = 0
        self.optionBuyPrice = 0
        self.currentPremiumValue = 0
        self.currentOrderID = ""
        self.target_reached = False

    def load_user_data(self):
        self.index_data = IndexDetails.objects.filter(index_name=self.index_name).values()
        self.user_broker_data = BrokerDetails.objects.filter(user_id=self.user_email,
                                                             index_group=self.index_group).values()
        self.user_scalper_details = ScalperDetails.objects.filter(user_id=self.user_email,
                                                                  index_name=self.index_name).values().first()

        self.user_target = self.user_scalper_details[TARGET]
        self.strike = self.user_scalper_details[STRIKE]
        self.lots = int(self.user_scalper_details[LOTS])
        self.qty = int(self.index_data[0][QTY])
        self.user_qty = self.qty * self.lots

    def initialize_broker(self):
        if self.user_broker_data:
            self.user_broker_details = self.user_broker_data[0]
            user_broker = self.user_broker_details[BROKER_NAME]
            self.is_demo_enabled = bool(self.user_scalper_details[IS_DEMO_TRADING_ENABLED])

            if user_broker == "angel_one":
                self.BrokerObject = AngelOneBroker(self.user_broker_data)
            elif user_broker == "kite":
                addLogDetails(INFO, "kite")
        else:
            raise Exception(STAGE_BROKER_NOT_PRESENT)

    def initialize_scalper(self):
        try:
            self.log_initialization()
            self.symbol_token = self.BrokerObject.getTokenForSymbol(BANKNIFTY_FUTURES)
            # self.started_time = current_time()[:-3]
            # self.started_date = datetime.today().strftime("%Y-%m-%d")
            self.started_time = "2024-07-19 13:45"
            self.started_date = "2024-07-19"
            self.adjust_start_time()

            while self.base_value is None:
                time.sleep(1)
                if not is_time_less_than_current_time(current_time()[:-3].split(" ")[1]):
                    candle_data = self.get_all_candle_data(self.started_time, self.to_time)
                    self.base_value = self.get_base_value(candle_data)
                    if self.base_value:
                        self.to_time = increaseTime(self.to_time, self.tf)
                else:
                    print("wait till market open")

            if self.base_value:
                self.monitor_market()
            else:
                print("base value is not set")
        except Exception as e:
            print(f"Error during scalper initialization: {e}")

    def log_initialization(self):
        addLogDetails(INFO, STAGE_STARTED)
        print(self.BrokerObject.checkProfile())

    def adjust_start_time(self):
        is_started_early = is_time_less_than_current_time(self.started_time.split(" ")[1])
        if is_started_early:
            self.started_time = f"{self.started_date} {NSE_OPEN_TIME}"
        self.to_time = increaseTime(self.started_time, self.tf)

    def get_base_value(self, data):
        if data is not None:
            base_value = data.iloc[-2]["close"]
            return base_value
        return None

    def get_all_candle_data(self, from_time, to_time):
        try:
            from_time = convert_datetime_string(from_time)
            to_time = convert_datetime_string(to_time)
            start_time = datetime(from_time['year'], from_time['month'], from_time['day'], from_time['hour'],
                                  from_time['minute'], from_time['second'])
            end_time = datetime(to_time['year'], to_time['month'], to_time['day'], to_time['hour'], to_time['minute'],
                                to_time['second'])

            candle_data = CandleData.objects.filter(time__range=(start_time, end_time))
            pd_data = list(candle_data.values('index_name', 'token', 'time', 'open', 'high', 'low', 'close'))

            df = pd.DataFrame(pd_data)
            df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].apply(pd.to_numeric,
                                                                                              errors='coerce')
            # print(df)

            return df
        except Exception as e:
            print(f"Error fetching candle data: {e}")

    def monitor_market(self):
        while not self.target_reached:
            time.sleep(1)
            candle_data = self.get_all_candle_data(self.started_time, self.to_time)
            if candle_data is not None:
                contains_next_candle = candle_data.map(lambda x: self.to_time.replace(" ", " ") in str(x)).any().any()
                if contains_next_candle:
                    self.place_order(candle_data)
                    self.to_time = increaseTime(self.to_time, self.tf)
                if self.isCEOrderPlaced or self.isPEOrderPlaced:
                    self.check_target_reached()
                if int(self.total_price) >= int(self.user_target):
                    addLogDetails(INFO, "stop scalper")
                    terminate_task(self.user_email, self.index_name, SCALPER)
                    break
            else:
                print("error in candle data")

    def place_order(self, candle_data):
        previous_close = self.get_base_value(candle_data)
        if previous_close > self.base_value:
            if not self.isCEOrderPlaced:
                self.exit_based_on_condition(self.currentPremiumValue, "place Call")
                self.place_call_option()
        elif previous_close < self.base_value:
            if not self.isPEOrderPlaced:
                self.exit_based_on_condition(self.currentPremiumValue, "Place put")
                self.place_put_option()

    def check_target_reached(self):
        addLogDetails(INFO, "order placed waiting for target")
        self.currentOptionPrice = self.BrokerObject.getLtpForPremium(self.optionDetails)
        if self.currentOptionPrice != CONNECTION_ERROR:
            if float(self.currentOptionPrice) + float(self.total_price) >= float(self.optionBuyPrice) + float(
                    self.user_target):
                self.exit_based_on_condition(self.currentPremiumValue, "target Reached")
                self.target_reached = True

    def place_call_option(self):
        self.currentPremiumPlaced = f"{getTradingSymbol(self.index_name)}{self.BrokerObject.getCurrentAtm(self.index_name) - int(self.strike)}CE"
        buy_order_details = self.create_order_details(BUY)
        self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
        self.process_order(buy_order_details, "CE")

    def place_put_option(self):
        self.currentPremiumPlaced = f"{getTradingSymbol(self.index_name)}{self.BrokerObject.getCurrentAtm(self.index_name) + int(self.strike)}PE"
        buy_order_details = self.create_order_details(BUY)
        self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
        self.process_order(buy_order_details, "PE")

    def create_order_details(self, transaction_type):
        return {
            VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: self.currentPremiumPlaced,
            SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(self.currentPremiumPlaced),
            TRANSACTION_TYPE: transaction_type, ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY,
            DURATION: DAY, QUANTITY: self.user_qty
        }

    def process_order(self, buy_order_details, order_type):
        if self.is_demo_enabled:
            order_response = self.place_dummy_order(order_type)
        else:
            order_response = self.BrokerObject.placeOrder(buy_order_details)
            addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} {order_response}")
            if order_response['message'] == 'SUCCESS':
                self.currentOrderID = order_response['data']['uniqueorderid']
                order_details = self.BrokerObject.getOrderDetails(self.currentOrderID)
                self.optionBuyPrice = order_details["averageprice"]
                data = {
                    USER_ID: self.user_email, SCRIPT_NAME: self.currentPremiumPlaced,
                    QTY: self.user_qty, ENTRY_PRICE: self.optionBuyPrice,
                    STATUS: ORDER_PLACED, STRATEGY: STRATEGY_SCALPER
                }
                addOrderBookDetails(data, True)

    def exit_based_on_condition(self, fromOptionPrice, reason):
        addLogDetails(INFO,
                      f"Index Name: {self.index_name} User: {self.user_email} Exit Based on condition called based on {reason}")
        try:
            if self.is_demo_enabled:
                self.revertDummyOrder(fromOptionPrice)
            else:
                if self.currentOrderID:
                    addLogDetails(INFO,
                                  f"Index Name: {self.index_name} User: {self.user_email} OrderId: {self.currentOrderID}")
                    if self.BrokerObject.checkIfOrderExists(self.currentOrderID):
                        sell_order_details = {
                            VARIETY: STOPLOSS,
                            EXCHANGE: NFO,
                            TRADING_SYMBOL: self.currentPremiumPlaced,
                            SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(self.currentPremiumPlaced),
                            TRANSACTION_TYPE: SELL,
                            ORDER_TYPE: MARKET,
                            PRODUCT_TYPE: INTRADAY,
                            DURATION: DAY,
                            QUANTITY: self.user_qty
                        }
                        initial_sell_order = self.BrokerObject.placeOrder(sell_order_details)
                        if initial_sell_order[MESSAGE] == 'SUCCESS':
                            sell_uniqueorderid = initial_sell_order["data"]["uniqueorderid"]
                            sell_price = self.BrokerObject.getOrderDetails(sell_uniqueorderid)["averageprice"]
                            self.total_price = float(sell_price) - float(self.optionBuyPrice)
                            data = {
                                USER_ID: self.user_email,
                                SCRIPT_NAME: self.currentPremiumPlaced,
                                QTY: self.user_qty,
                                EXIT_PRICE: sell_price,
                                STATUS: ORDER_EXITED
                            }
                            addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} {data}")
                            addOrderBookDetails(data, False)
        except Exception as e:
            addLogDetails(ERROR, f"{self.index_name} exception in exitBasedOnCondition ----- {str(e)}")

    def revertDummyOrder(self, fromOptionPrice):
        if self.isCEOrderPlaced or self.isPEOrderPlaced:
            addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} revertDummyOrder")
            order_response = {'message': 'SUCCESS', 'data': {'order_id': 'exit_dummy_id'}}
            self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
            exit_price = self.BrokerObject.getLtpForPremium(self.optionDetails)
            data = {
                USER_ID: self.user_email,
                SCRIPT_NAME: self.currentPremiumPlaced,
                QTY: self.user_qty,
                EXIT_PRICE: exit_price,
                STATUS: ORDER_EXITED
            }
            addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} {data}")
            addOrderBookDetails(data, False)
            self.total_price = float(exit_price) - float(self.optionBuyPrice)
            self.isPEOrderPlaced = False
            self.isCEOrderPlaced = False
            return order_response
        else:
            addLogDetails(INFO, "No dummy orders present")

    def place_dummy_order(self, orderType):
        try:
            addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} placeDummyOrder")
            order_response = {'message': 'SUCCESS', 'data': {'orderid': 'dummy_id'}}
            self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
            self.optionBuyPrice = self.BrokerObject.getLtpForPremium(self.optionDetails)
            data = {
                USER_ID: self.user_email,
                SCRIPT_NAME: self.currentPremiumPlaced,
                QTY: self.user_qty,
                ENTRY_PRICE: self.optionBuyPrice,
                STATUS: ORDER_PLACED,
                STRATEGY: STRATEGY_SCALPER
            }
            addOrderBookDetails(data, True)
            if orderType == "CE":
                self.isCEOrderPlaced = True
                self.isPEOrderPlaced = False
                print(f"dummy order isCEOrderPlaced {self.isCEOrderPlaced}")
            elif orderType == "PE":
                self.isPEOrderPlaced = True
                self.isCEOrderPlaced = False
                print(f"dummy order isPEOrderPlaced {self.isPEOrderPlaced}")
            self.currentOrderID = order_response['data']['orderid']
            return order_response
        except Exception as e:
            addLogDetails(ERROR, f"User: {self.user_email} exception in placeDummyOrder ----- {str(e)}")
