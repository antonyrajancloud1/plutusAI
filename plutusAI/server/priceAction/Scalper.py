import time

from plutusAI.server.base import *
from plutusAI.server.broker.AngelOneBroker import AngelOneBroker


class Scalper():
    def __init__(self, user_email, index, index_group):
        self.started_time = None
        self.exchange = "NSE"
        self.base_value = None
        self.to_time = None
        self.tf = 1
        self.isCEOrderPlaced = False
        self.isPEOrderPlaced = False
        self.currentPremiumPlaced = None
        self.total_price = 0
        self.optionBuyPrice = 0
        self.qty = 1
        self.currentPremiumValue = 0

        try:
            print("ZZZZZZZZZZZ")
            self.user_email = user_email
            self.index_name = index
            self.index_group = index_group
            self.index_data = IndexDetails.objects.filter(index_name=index)
            self.user_broker_data = BrokerDetails.objects.filter(user_id=user_email, index_group=self.index_group)
            self.user_scalper_details = ScalperDetails.objects.filter(user_id=user_email, index_name=self.index_name)
            self.index_data = list(self.index_data.values())
            self.user_broker_details = list(self.user_broker_data.values())
            self.user_scalper_details = list(self.user_scalper_details.values())[0]
            print(self.user_scalper_details)
            self.user_target = self.user_scalper_details[TARGET]
            self.strike = self.user_scalper_details[STRIKE]
            print(self.strike)
            if len(self.user_broker_details) > 0:
                self.user_broker_details = self.user_broker_details[0]
                user_broker = self.user_broker_details[BROKER_NAME]
                self.is_demo_enabled = bool(self.user_scalper_details[IS_DEMO_TRADING_ENABLED])
                print(user_broker)
                match user_broker:
                    case "angel_one":
                        self.BrokerObject = AngelOneBroker(self.user_broker_data)
                    case "kite":
                        addLogDetails(INFO, "kite")
                self.initilize_scalper()
            else:
                # updateIndexConfiguration(user_email=self.user_email,index=self.index_name,data=STAGE_BROKER_NOT_PRESENT)
                print(STAGE_BROKER_NOT_PRESENT)
        except Exception as e:
            addLogDetails(ERROR, str(e))

    def initilize_scalper(self):
        print(STAGE_STARTED)
        print(self.BrokerObject.checkProfile())
        # from_time = "2024-06-28 09:15"
        # to_time = "2024-06-28 14:26"
        count = 0
        self.symbol_token = 99926009
        # self.started_time = "2024-06-28 09:14"
        self.started_time = current_time()[:-3]
        self.started_date = datetime.today().strftime("%Y-%m-%d")
        # self.started_date = "2024-06-28"

        print(self.started_time)
        is_started_early = is_time_less_than_current_time(self.started_time.split(" ")[1])
        if is_started_early:
            self.started_time = self.started_date + " " + NSE_OPEN_TIME
        print(self.started_time)
        self.to_time = increaseTime(self.started_time, self.tf)
        print(self.to_time)
        while True:
            print( "waiting for basevalue")
            candle_data = self.getAllCandleData(self.started_time, self.to_time)
            self.base_value = self.getBaseValueUsingStartTime(candle_data)
            if self.base_value is not None:
                self.to_time = increaseTime(self.started_time, self.tf)
                break
        # print(increaseTime(self.to_time, self.tf))
        if self.base_value is not None:
            is_target_reached = self.total_price >= self.user_target
            while True:
                candle_data = self.getAllCandleData(self.started_time, self.to_time)

                print(self.to_time)
                print(candle_data)
                contains_next_candle = candle_data.applymap(
                    lambda x: self.to_time.replace(" ", "T") in str(x)).any().any()
                if contains_next_candle:
                    previous_close = self.getBaseValueUsingStartTime(candle_data)
                    if previous_close > self.base_value:
                        if not self.isCEOrderPlaced:
                            print("place call")
                            self.exitBasedOnCondition(self.currentPremiumValue, "target Reached")
                            self.placeCallOption()
                    elif previous_close < self.base_value:
                        if not self.isPEOrderPlaced:
                            print("place put")
                            self.exitBasedOnCondition(self.currentPremiumValue, "target Reached")
                            self.placePutOption()
                    elif self.isCEOrderPlaced or self.isPEOrderPlaced:
                        self.currentOptionPrice = self.BrokerObject.getLtpForPremium(self.optionDetails)
                        if self.currentPremiumValue >= self.user_target:
                            self.exitBasedOnCondition(self.currentPremiumValue, "target Reached")
                    self.to_time = increaseTime(self.started_time, self.tf)
                elif is_target_reached:
                    print("stop scalper")

                break
        else:
            print("base value is not set")

        # while True:
        #
        #     self.BrokerObject.getCandleData("NSE",99926009,from_time,to_time)
        #     count+=1
        #     print(count)
        #     time.sleep(0.5)
        #     if count > 10000:
        #         break

    def getBaseValueUsingStartTime(self, data):
        try:
            print(data.__len__())
            base_value = data.iloc[-2]["close"]
            print("data for base >>>> " + str(base_value))
            return base_value
        except Exception as e:
            print(e)

    def getAllCandleData(self, from_time, to_time):
        # print(from_time)
        # print(to_time)
        # from_time = "2024-06-28 09:15"
        # to_time = "2024-06-28 14:26"
        time.sleep(0.5)
        return self.BrokerObject.getCandleData(self.exchange, self.symbol_token, from_time, to_time)

    def placeCallOption(self):
        self.currentPremiumPlaced = getTradingSymbol(self.index_name) + str(
            self.BrokerObject.getCurrentAtm(self.index_name) - self.strike) + "CE"
        buy_order_details = {VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: self.currentPremiumPlaced,
                             SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(self.currentPremiumPlaced),
                             TRANSACTION_TYPE: BUY, ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY, DURATION: DAY,
                             QUANTITY: self.qty}
        self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
        if self.is_demo_enabled:
            order_response = self.placeDummyOrder("CE")
        else:
            order_response = self.BrokerObject.placeOrder(buy_order_details)
            addLogDetails(INFO, "Index Name: " + self.index_name + " User :" + self.user_email + " " + str(
                order_response))
            if order_response['message'].__eq__('SUCCESS'):
                self.currentOrderID = order_response['data']['uniqueorderid']
                uniqueorderid = order_response["data"]["uniqueorderid"]
                order_details = self.BrokerObject.getOrderDetails(uniqueorderid)
                self.optionBuyPrice = order_details["averageprice"]
                data = {USER_ID: self.user_email, SCRIPT_NAME: self.currentPremiumPlaced, QTY: self.qty,
                        ENTRY_PRICE: self.optionBuyPrice, STATUS: ORDER_PLACED, STRATEGY: STRATEGY_HUNTER}
                addOrderBookDetails(data, True)
                self.isCEOrderPlaced = True

    def placePutOption(self):
        self.currentPremiumPlaced = getTradingSymbol(self.index_name) + str(
            self.BrokerObject.getCurrentAtm(self.index_name) + self.strike) + "PE"
        buy_order_details = {VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: self.currentPremiumPlaced,
                             SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(self.currentPremiumPlaced),
                             TRANSACTION_TYPE: BUY, ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY, DURATION: DAY,
                             QUANTITY: self.qty}
        self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
        if self.is_demo_enabled:
            order_response = self.placeDummyOrder("PE")
        else:
            order_response = self.BrokerObject.placeOrder(buy_order_details)
            addLogDetails(INFO, "Index Name: " + self.index_name + " User :" + self.user_email + " " + str(
                order_response))
            if order_response['message'].__eq__('SUCCESS'):
                self.currentOrderID = order_response['data']['uniqueorderid']
                uniqueorderid = order_response["data"]["uniqueorderid"]
                order_details = self.BrokerObject.getOrderDetails(uniqueorderid)
                self.optionBuyPrice = order_details["averageprice"]
                data = {USER_ID: self.user_email, SCRIPT_NAME: self.currentPremiumPlaced, QTY: self.qty,
                        ENTRY_PRICE: self.optionBuyPrice, STATUS: ORDER_PLACED, STRATEGY: STRATEGY_HUNTER}
                addOrderBookDetails(data, True)
                self.isPEOrderPlaced = True

    def exitBasedOnCondition(self, fromOptionPrice, reason):
        addLogDetails(INFO,
                      "Index Name: " + self.index_name + " User : " + self.user_email + " Exit Based on condition called based on " + reason)
        try:
            if self.is_demo_enabled:
                self.revertDummyOrder(fromOptionPrice)
            else:
                if self.currentOrderID != "":
                    addLogDetails(INFO,
                                  "Index Name: " + self.index_name + " User :" + self.user_email + " OrderId: " + self.currentOrderID)
                    if self.BrokerObject.checkIfOrderExists(self.currentOrderID):
                        sell_order_details = {VARIETY: STOPLOSS, EXCHANGE: NFO,
                                              TRADING_SYMBOL: self.currentPremiumPlaced,
                                              SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(
                                                  self.currentPremiumPlaced),
                                              TRANSACTION_TYPE: SELL, ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY,
                                              DURATION: DAY,
                                              QUANTITY: self.qty}
                        initial_sell_order = self.BrokerObject.placeOrder(sell_order_details)
                        if initial_sell_order[MESSAGE].__eq__('SUCCESS'):
                            sell_uniqueorderid = initial_sell_order["data"]["uniqueorderid"]
                            sell_price = self.BrokerObject.getOrderDetails(sell_uniqueorderid)["averageprice"]
                            self.total_price = float(sell_price) - float(self.optionBuyPrice)
        except Exception as e:
            addLogDetails(ERROR, str(self.index_name) + "exception in exitBasedOnCondition  -----  " + str(e))

    def placeDummyOrder(self, orderType):
        try:
            addLogDetails(INFO, "Index Name: " + self.index_name + " User :" + self.user_email + " placeDummyOrder")
            order_response = {'message': 'SUCCESS', 'data': {'orderid': 'dummy_id'}}
            self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
            self.optionBuyPrice = self.BrokerObject.getLtpForPremium(self.optionDetails)
            data = {USER_ID: self.user_email, SCRIPT_NAME: self.currentPremiumPlaced, QTY: self.qty,
                    ENTRY_PRICE: self.optionBuyPrice, STATUS: ORDER_PLACED, STRATEGY: STRATEGY_SCALPER}
            # addLogDetails(INFO, "data fine")
            # addOrderBookDetails(data, True)
            if orderType == "CE":
                self.isCEOrderPlaced = True
            elif orderType == "PE":
                self.isPEOrderPlaced = True
            self.currentOrderID = order_response['data']['orderid']

            return order_response
        except Exception as e:
            addLogDetails(ERROR, "User :" + self.user_email + " exception in placeDummyOrder  -----  " + str(e))

    def revertDummyOrder(self, fromOptionPrice):
        addLogDetails(INFO, "Index Name: " + self.index_name + " User :" + self.user_email + " revertDummyOrder")
        order_response = {'message': 'SUCCESS', 'data': {'order_id': 'exit_dummy_id'}}
        self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
        data = {USER_ID: self.user_email, SCRIPT_NAME: self.currentPremiumPlaced, QTY: self.qty,
                EXIT_PRICE: self.BrokerObject.getLtpForPremium(self.optionDetails), STATUS: ORDER_EXITED}
        addLogDetails(INFO, "Index Name: " + self.index_name + " User :" + self.user_email + " " + str(data))
        addOrderBookDetails(data, False)
        self.isPEOrderPlaced = False
        self.isCEOrderPlaced = False
        return order_response
