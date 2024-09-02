import time
from math import trunc

from django.db.models import Q

from plutusAI.server.base import *
from plutusAI.server.broker.AngelOneBroker import AngelOneBroker
from plutusAI.server.broker.Broker import Broker


# from plutusAI.views import stop_current_celery_task
# def stop_current_celery_task(user_email,index_name,strategy):
#     terminate_task(user_email, index_name, strategy)

class Scalper():
    def __init__(self, user_email, index, index_group):
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
        # self.qty = 1
        self.currentPremiumValue = 0
        self.currentOrderID = ""
        self.target_reached = False

        try:
            # checkSocketStatus()
            self.user_email = user_email
            self.index_name = index
            self.index_group = index_group
            self.index_data = IndexDetails.objects.filter(index_name=index)
            # self.user_broker_data = BrokerDetails.objects.filter(user_id=user_email, index_group=self.index_group)
            self.user_scalper_details = ScalperDetails.objects.filter(user_id=user_email, index_name=self.index_name)
            self.index_data = list(self.index_data.values())
            # self.user_broker_details = list(self.user_broker_data.values())
            self.user_scalper_details = list(self.user_scalper_details.values())[0]
            print(self.user_scalper_details)
            self.user_target = self.user_scalper_details[TARGET]
            self.strike = self.user_scalper_details[STRIKE]
            self.lots = int(self.user_scalper_details[LOTS])
            self.qty = int(self.index_data[0][QTY])
            self.user_qty = int(self.qty) * int(self.lots)
            self.on_candle_close = self.user_scalper_details[ON_CANDLE_CLOSE]
            print(self.strike)
            # if len(self.user_broker_details) > 0:
            #     self.user_broker_details = self.user_broker_details[0]
            #     user_broker = self.user_broker_details[BROKER_NAME]
            #     self.is_demo_enabled = bool(self.user_scalper_details[IS_DEMO_TRADING_ENABLED])
            #     print(self.is_demo_enabled)
            #     match user_broker:
            #         case "angel_one":
            #             self.BrokerObject = AngelOneBroker(self.user_broker_data)
            #         case "kite":
            #             addLogDetails(INFO, "kite")
            self.BrokerObject = Broker(self.user_email, self.index_group).BrokerObject
            self.is_demo_enabled = self.BrokerObject.is_demo_enabled
            print(self.is_demo_enabled)
            if self.BrokerObject.checkProfile()[MESSAGE] == "SUCCESS":
                self.initilize_scalper()
            else:
                # updateIndexConfiguration(user_email=self.user_email,index=self.index_name,data=STAGE_BROKER_NOT_PRESENT)
                print(STAGE_BROKER_NOT_PRESENT)
        except Exception as e:
            addLogDetails(ERROR, str(e))

    def initilize_scalper(self):
        try:
            updateScalperDetails(self.user_email, self.index_name, data=STAGE_STARTED)
            print(self.BrokerObject.checkProfile())
            # from_time = "2024-06-28 09:15"
            # to_time = "2024-06-28 14:26"
            count = 0
            self.symbol_token = self.BrokerObject.getTokenForSymbol(BANKNIFTY_FUTURES)
            # self.symbol_token = "35165"

            # self.started_time = "2024-07-10 09:14"
            # self.started_date = "2024-07-10"
            # self.started_time = "2024-07-19 13:45"
            # self.started_date = "2024-07-19"
            self.started_time = current_time()[:-3]
            self.started_date = datetime.today().strftime("%Y-%m-%d")
            print(self.started_time)
            is_started_early = is_time_less_than_current_time(self.started_time.split(" ")[1])
            if is_started_early:
                self.started_time = self.started_date + " " + NSE_OPEN_TIME
            print(self.started_time)
            self.to_time = increaseTime(self.started_time, self.tf)
            print(self.to_time)
            while self.base_value is None:
                # print(getCurrentIndexValue(str(self.index_name)+"_fut"))
                time.sleep(1)
                if not is_time_less_than_current_time(current_time()[:-3].split(" ")[1]):
                    print("waiting for basevalue")
                    candle_data = self.getAllCandleData(self.started_time, self.to_time)
                    self.base_value = self.getBaseValueUsingStartTime(candle_data)
                    # if self.base_value is not None:
                    #     self.to_time = increaseTime(self.to_time, self.tf)
                    #     print("increased time = "+ str(self.to_time))
                else:
                    print("wait till market open")
            if self.on_candle_close:
                self.scalperOnCandleClose()
            else :
                self.scalperOnBaseValue()



        except Exception as e:
            print(e)

    def scalperOnCandleClose(self):
        if self.base_value is not None:
            print(self.user_target)
            self.target_reached = (int(self.total_price).__ge__(int(self.user_target)))
            while not self.target_reached:
                time.sleep(1)
                candle_data = self.getAllCandleData(self.started_time, self.to_time)
                print(candle_data)
                if candle_data is not None:
                    contains_next_candle = candle_data.map(
                        lambda x: self.to_time in str(x)).any().any()
                    print(contains_next_candle)
                    print(self.to_time)
                    if contains_next_candle:
                        previous_close = self.getBaseValueUsingStartTime(candle_data)
                        if previous_close > self.base_value:
                            if not self.isCEOrderPlaced:
                                self.user_target = float(self.user_target)  + getBrokerageForLots(self.lots, self.qty)
                                self.exitBasedOnCondition(self.currentPremiumValue, "place Call")
                                self.placeCallOption()
                                updateScalperDetails(self.user_email, self.index_name, data=STAGE_LONG)
                        elif previous_close < self.base_value:
                            if not self.isPEOrderPlaced:
                                self.user_target =float(self.user_target)  + getBrokerageForLots(self.lots, self.qty)
                                self.exitBasedOnCondition(self.currentPremiumValue, "Place put")
                                self.placePutOption()
                                updateScalperDetails(self.user_email, self.index_name, data=STAGE_SHORT)

                        self.to_time = increaseTime(self.to_time, self.tf)

                    if self.isCEOrderPlaced or self.isPEOrderPlaced:
                        addLogDetails(INFO, "order placed waiting for target")
                        self.currentOptionPrice = self.BrokerObject.getLtpForPremium(self.optionDetails)
                        if self.currentOptionPrice is not CONNECTION_ERROR:
                            if float(self.currentOptionPrice) + float(self.total_price) >= float(
                                    self.optionBuyPrice) + float(self.user_target):
                                print(" target reached" + str(
                                    float(self.currentOptionPrice) + float(self.total_price)))
                                self.exitBasedOnCondition(self.currentPremiumValue, "target Reached")
                                self.target_reached = True
                                # break
                    if self.target_reached:
                        addLogDetails(INFO, "stop scalper")
                        terminate_task(self.user_email, self.index_name, SCALPER)
                        break

                else:
                    print("error in candle data")

        else:
            print("base value is not set")

    def scalperOnBaseValue(self):
        if self.base_value is not None:
            print(self.user_target)
            self.target_reached = (int(self.total_price).__ge__(int(self.user_target)))
            while not self.target_reached:
                time.sleep(1)
                candle_data = self.getAllCandleData(self.started_time, self.to_time)
                if candle_data is not None:
                    contains_next_candle = candle_data.map(
                        lambda x: self.to_time in str(x)).any().any()
                    print(contains_next_candle)
                    print(self.to_time)
                    if contains_next_candle:
                        if getCurrentIndexValue(str(self.index_name)+"_fut") > self.base_value:
                            if not self.isCEOrderPlaced:
                                self.user_target  = float(self.user_target)  + getBrokerageForLots(self.lots, self.qty)
                                self.exitBasedOnCondition(self.currentPremiumValue, "place Call")
                                self.placeCallOption()
                                updateScalperDetails(self.user_email, self.index_name, data=STAGE_LONG)
                        elif getCurrentIndexValue(str(self.index_name)+"_fut") < self.base_value:
                            if not self.isPEOrderPlaced:
                                self.user_target = float(self.user_target)  + getBrokerageForLots(self.lots, self.qty)
                                self.exitBasedOnCondition(self.currentPremiumValue, "Place put")
                                self.placePutOption()
                                updateScalperDetails(self.user_email, self.index_name, data=STAGE_SHORT)
                        if self.isCEOrderPlaced or self.isPEOrderPlaced:
                            addLogDetails(INFO, "order placed waiting for target")
                            self.currentOptionPrice = self.BrokerObject.getLtpForPremium(self.optionDetails)
                            if self.currentOptionPrice is not CONNECTION_ERROR:
                                if float(self.currentOptionPrice) + float(self.total_price) >= float(
                                        self.optionBuyPrice) + float(self.user_target):
                                    print(" target reached" + str(
                                        float(self.currentOptionPrice) + float(self.total_price)))
                                    self.exitBasedOnCondition(self.currentPremiumValue, "target Reached")
                                    self.target_reached = True
                        if self.target_reached:
                            addLogDetails(INFO, "stop scalper")
                            terminate_task(self.user_email, self.index_name, SCALPER)
                            break


                else:
                    print("error in candle data")

        else:
            print("base value is not set")
    def getBaseValueUsingStartTime(self, data):
        global base_value
        try:
            if data is not None:
                print(data.__len__())
                base_value = data.iloc[-1]["close"]
                print("data for base >>>> " + str(base_value))
            else:
                print("No Data")
                base_value = None
            return base_value

        except Exception as e:
            print(e)

    def getAllCandleData(self, from_time, to_time):
        try:
            # from_time = "2024-07-19 13:45"
            # to_time = "2024-07-19 13:46"

            from_time = convert_datetime_string(from_time)
            to_time = convert_datetime_string(to_time)

            start_time = datetime(from_time['year'], from_time['month'], from_time['day'], from_time['hour'],
                                  from_time['minute'], from_time['second'])
            end_time = datetime(to_time['year'], to_time['month'], to_time['day'], to_time['hour'], to_time['minute'],
                                to_time['second'])
            candle_data = CandleData.objects.filter(time__range=(start_time, end_time))
            # print(candle_data.count())
            # for d in candle_data:
            #     print(d)
            # candle_data = CandleData.objects.filter(time__range=(convert_datetime_string(from_time), convert_datetime_string(to_time)))
            # for d in candle_data:
            #     print(d)
            pd_data = list(candle_data.values('index_name', 'token', 'time', 'open', 'high', 'low', 'close'))
            # Convert list of dictionaries to DataFrame
            df = pd.DataFrame(pd_data)
            # Convert fields to appropriate types (optional, if needed)
            df['open'] = pd.to_numeric(df['open'], errors='coerce')
            df['high'] = pd.to_numeric(df['high'], errors='coerce')
            df['low'] = pd.to_numeric(df['low'], errors='coerce')
            df['close'] = pd.to_numeric(df['close'], errors='coerce')
            # print(df)
            return df

            # return self.BrokerObject.getCandleData(self.exchange, self.symbol_token, from_time, to_time)
        except Exception as e:
            print(e)

    def placeCallOption(self):
        self.currentPremiumPlaced = getTradingSymbol(self.index_name) + str(
            self.BrokerObject.getCurrentAtm(self.index_name) - int(self.strike)) + "CE"
        buy_order_details = {VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: self.currentPremiumPlaced,
                             SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(self.currentPremiumPlaced),
                             TRANSACTION_TYPE: BUY, ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY, DURATION: DAY,
                             QUANTITY: self.user_qty}
        self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
        print(buy_order_details)
        print(self.optionDetails)
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
                print(order_details)
                self.optionBuyPrice = order_details["averageprice"]
                data = {USER_ID: self.user_email, SCRIPT_NAME: self.currentPremiumPlaced, QTY: self.user_qty,
                        ENTRY_PRICE: self.optionBuyPrice, STATUS: ORDER_PLACED, STRATEGY: STRATEGY_HUNTER,
                        INDEX_NAME: self.index_name}
                addOrderBookDetails(data, True)
                self.isCEOrderPlaced = True
                trigger_price = round(float(self.optionBuyPrice)+ float(self.total_price) + float(self.user_target),1)
                price = trigger_price + 0
                sell_order_details = {VARIETY: STOPLOSS, EXCHANGE: NFO, TRADING_SYMBOL: self.currentPremiumPlaced,
                                      SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(self.currentPremiumPlaced),
                                      TRANSACTION_TYPE: SELL, ORDER_TYPE: ORDER_TYPE_SL, PRICE: price,
                                      TRIGGER_PRICE: trigger_price, PRODUCT_TYPE: INTRADAY, DURATION: DAY,
                                      QUANTITY: self.user_qty}
                sell_order_response = self.BrokerObject.placeOrder(sell_order_details)
                addLogDetails(INFO, sell_order_details)
                addLogDetails(INFO, sell_order_response)

                if sell_order_response['message'].__eq__('SUCCESS'):
                    self.currentOrderID = sell_order_response['data']['uniqueorderid']
                    self.orderid = sell_order_response['data']['orderid']
                    sell_order_response_details = self.BrokerObject.getOrderDetails(self.currentOrderID)
                    addLogDetails(INFO, sell_order_response_details)


    def placePutOption(self):
        self.currentPremiumPlaced = getTradingSymbol(self.index_name) + str(
            self.BrokerObject.getCurrentAtm(self.index_name) + int(self.strike)) + "PE"
        buy_order_details = {VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: self.currentPremiumPlaced,
                             SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(self.currentPremiumPlaced),
                             TRANSACTION_TYPE: BUY, ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY, DURATION: DAY,
                             QUANTITY: self.user_qty}
        self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
        print(buy_order_details)
        print(self.optionDetails)
        if self.is_demo_enabled:
            order_response = self.placeDummyOrder("PE")
        else:
            order_response = self.BrokerObject.placeOrder(buy_order_details)
            addLogDetails(INFO, "Index Name: " + self.index_name + " User :" + self.user_email + " " + str(
                order_response))
            if order_response['message'].__eq__('SUCCESS'):
                self.currentOrderID = order_response['data']['uniqueorderid']
                addLogDetails(INFO,"self.currentOrderID = "+str(self.currentOrderID))
                uniqueorderid = order_response["data"]["uniqueorderid"]

                order_details = self.BrokerObject.getOrderDetails(uniqueorderid)
                print(order_details)
                self.optionBuyPrice = order_details["averageprice"]
                data = {USER_ID: self.user_email, SCRIPT_NAME: self.currentPremiumPlaced, QTY: self.qty,
                        ENTRY_PRICE: self.optionBuyPrice, STATUS: ORDER_PLACED, STRATEGY: STRATEGY_HUNTER,
                        INDEX_NAME: self.index_name}
                addOrderBookDetails(data, True)
                self.isPEOrderPlaced = True

                trigger_price = round(float(self.optionBuyPrice)+ float(self.total_price) + float(self.user_target),1)
                price = trigger_price +0
                sell_order_details = {VARIETY: STOPLOSS, EXCHANGE: NFO, TRADING_SYMBOL: self.currentPremiumPlaced,
                                      SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(self.currentPremiumPlaced),
                                      TRANSACTION_TYPE: SELL, ORDER_TYPE: ORDER_TYPE_SL, PRICE: price,
                                      TRIGGER_PRICE: trigger_price, PRODUCT_TYPE: INTRADAY, DURATION: DAY,
                                      QUANTITY: self.user_qty}

                sell_order_response = self.BrokerObject.placeOrder(sell_order_details)
                addLogDetails(INFO,sell_order_details)
                addLogDetails(INFO, sell_order_response)
                if sell_order_response['message'].__eq__('SUCCESS'):
                    self.currentOrderID = sell_order_response['data']['uniqueorderid']
                    self.orderid = sell_order_response['data']['orderid']

                    addLogDetails(INFO, "self.currentOrderID = " + str(self.currentOrderID))
                    sell_order_response_details = self.BrokerObject.getOrderDetails(self.currentOrderID)
                    addLogDetails(INFO, sell_order_response_details)

    def exitBasedOnCondition(self, fromOptionPrice, reason):
        addLogDetails(INFO,
                      "Index Name: " + self.index_name + " User : " + self.user_email + " Exit Based on condition called based on " + reason)
        try:
            if self.is_demo_enabled:
                self.revertDummyOrder(fromOptionPrice)
            else:
                addLogDetails(INFO," self.currentOrderID = " +str(self.currentOrderID))
                if self.currentOrderID != "":
                    addLogDetails(INFO,
                                  "Index Name: " + self.index_name + " User :" + self.user_email + " OrderId: " + self.currentOrderID)
                    if self.BrokerObject.checkIfOrderExists(self.currentOrderID):
                        addLogDetails(INFO,"currentOrderID is present "+str(self.currentOrderID))
                        modify_order_details = {ORDERID: self.orderid, VARIETY: NORMAL, EXCHANGE: NFO,
                                                TRADING_SYMBOL: self.currentPremiumPlaced,SYMBOL_TOKEN:self.BrokerObject.getTokenForSymbol(self.currentPremiumPlaced), TRANSACTION_TYPE: SELL,
                                                ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY, DURATION: DAY,
                                                QUANTITY: self.user_qty}
                        addLogDetails(INFO,modify_order_details)
                        modifyOrder_response = self.BrokerObject.modifyOrder(modify_order_details)

                        addLogDetails(INFO,"modifyOrder_response = "+str(modifyOrder_response))

                    else:
                        addLogDetails(INFO,"self.BrokerObject.checkIfOrderExists is false")
                        addLogDetails(INFO,self.BrokerObject.checkIfOrderExists(self.currentOrderID))

                    sell_price = self.BrokerObject.getOrderDetails(self.currentOrderID)["averageprice"]
                    self.total_price = float(self.total_price) + float(sell_price) - float(self.optionBuyPrice)
                    self.isPEOrderPlaced = False
                    self.isCEOrderPlaced = False
                    data = {USER_ID: self.user_email, SCRIPT_NAME: self.currentPremiumPlaced,
                            QTY: self.user_qty, EXIT_PRICE: sell_price, STATUS: ORDER_EXITED}
                    addLogDetails(INFO,
                                  "Index Name: " + self.index_name + " User :" + self.user_email + " " + str(
                                      data))
                    addOrderBookDetails(data, False)

        except Exception as e:
            addLogDetails(ERROR, str(self.index_name) + "exception in exitBasedOnCondition  -----  " + str(e))

    def placeDummyOrder(self, orderType):
        try:
            addLogDetails(INFO, "Index Name: " + self.index_name + " User :" + self.user_email + " placeDummyOrder")
            order_response = {'message': 'SUCCESS', 'data': {'orderid': 'dummy_id'}}
            self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
            self.optionBuyPrice = self.BrokerObject.getLtpForPremium(self.optionDetails)
            data = {USER_ID: self.user_email, SCRIPT_NAME: self.currentPremiumPlaced, QTY: self.user_qty,
                    ENTRY_PRICE: self.optionBuyPrice, STATUS: ORDER_PLACED, STRATEGY: STRATEGY_SCALPER,
                    INDEX_NAME: self.index_name}
            # addLogDetails(INFO, "data fine")
            addOrderBookDetails(data, True)
            if orderType == "CE":
                self.isCEOrderPlaced = True
                self.isPEOrderPlaced = False
                print("dummy order isCEOrderPlaced " + str(self.isCEOrderPlaced))
            elif orderType == "PE":
                self.isPEOrderPlaced = True
                self.isCEOrderPlaced = False
                print("dummy order isPEOrderPlaced " + str(self.isPEOrderPlaced))
            self.currentOrderID = order_response['data']['orderid']

            return order_response
        except Exception as e:
            addLogDetails(ERROR, "User :" + self.user_email + " exception in placeDummyOrder  -----  " + str(e))

    def revertDummyOrder(self, fromOptionPrice):
        if self.isCEOrderPlaced or self.isPEOrderPlaced:
            # self.total_price = self.total_price + getBrokerageForLots(self.lots, self.qty)
            addLogDetails(INFO, "Index Name: " + self.index_name + " User :" + self.user_email + " revertDummyOrder")
            order_response = {'message': 'SUCCESS', 'data': {'order_id': 'exit_dummy_id'}}
            self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
            data = {USER_ID: self.user_email, SCRIPT_NAME: self.currentPremiumPlaced, QTY: self.user_qty,
                    EXIT_PRICE: self.BrokerObject.getLtpForPremium(self.optionDetails), STATUS: ORDER_EXITED}
            addLogDetails(INFO, "Index Name: " + self.index_name + " User :" + self.user_email + " " + str(data))
            addOrderBookDetails(data, False)
            self.total_price = float(self.total_price) + (float(data[EXIT_PRICE]) - float(self.optionBuyPrice))
            self.isPEOrderPlaced = False
            self.isCEOrderPlaced = False
            return order_response
        else:
            addLogDetails(INFO, "No dummy orders present")

