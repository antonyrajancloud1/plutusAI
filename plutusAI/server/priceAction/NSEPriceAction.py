from plutusAI.models import JobDetails
from plutusAI.server.AngelOneApp import *
from plutusAI.server.base import *
from plutusAI.server.broker.AngelOneBroker import AngelOneBroker
from plutusAI.server.constants import *
from plutusAI.server.priceAction.priceActionScalper import *


class NSEPriceAction:

    def __init__(self, user_email, index, index_group):
        try:
            self.strategy = STRATEGY_HUNTER
            self.user_email = user_email
            self.index_name = index
            self.index_group = index_group
            self.user_data = Configuration.objects.filter(user_id=user_email, index_name=index)
            self.index_data = IndexDetails.objects.filter(index_name=index)
            self.user_broker_data = BrokerDetails.objects.filter(user_id=user_email, index_group=index_group)

            self.index_data = list(self.index_data.values())
            self.config_data = list(self.user_data.values())
            self.user_broker_details = list(self.user_broker_data.values())

            if self.user_broker_details:
                self.user_broker_details = self.user_broker_details[0]
                user_broker = self.user_broker_details[BROKER_NAME]
                self.is_demo_enabled = bool(self.user_broker_details[IS_DEMO_TRADING_ENABLED])
                if user_broker == "angel_one":
                    self.BrokerObject = AngelOneBroker(self.user_broker_data)
                elif user_broker == "kite":
                    addLogDetails(INFO, "kite")

                if self.config_data:
                    self.config_data = self.config_data[0]
                    self.levels = convert_string_to_int_array(str(self.config_data[LEVELS]).split(','))
                    self.index_trend_check = float(self.config_data[TREND_CHECK_POINTS])
                    self.index_trailing = float(self.config_data[TRAILING_POINTS])
                    self.lots = int(self.config_data[LOTS])
                    self.qty = int(self.index_data[0][QTY])
                    self.strike = int(self.config_data[STRIKE])
                    self.user_qty = self.qty * self.lots
                    self.initialSL = int(self.config_data[INITIAL_SL])
                    self.targetforsafesl = int(self.config_data[TARGET_FOR_SAFE_SL])
                    self.safe_sl = int(self.config_data[SAFE_SL])
                    self.timeInterval = 1
                    self.initilize_price_action()
            else:
                updateIndexConfiguration(user_email=self.user_email, index=self.index_name,
                                         data=STAGE_BROKER_NOT_PRESENT)
        except Exception as e:
            addLogDetails(ERROR, str(e))

    def initDefaultValues(self):
        self.exitConditions = []
        self.isCEOrderPlaced = False
        self.isTrailStoplossPlaced = False
        self.isPEOrderPlaced = False
        self.indexBaseValue = 0
        self.nearestSupport = 0
        self.nearestResistance = 0
        self.IndexLTP = 0
        self.optionExitPrice = 0
        self.isOrderExited = False

    def initilize_price_action(self):
        updateIndexConfiguration(user_email=self.user_email, index=self.index_name, data=STAGE_STARTED)
        self.initDefaultValues()
        self.indexBaseValue = getCurrentIndexValue(self.index_name)
        self.nearestSupport = getTaregtForOrderFromList(self.levels, self.indexBaseValue, "PE")
        self.nearestResistance = getTaregtForOrderFromList(self.levels, self.indexBaseValue, "CE")
        self.mainSchedulerText = (
            f"Job started for User: {self.user_email} Index Name: {self.index_name}\t"
            f"nearestSupport == {self.nearestSupport}\tnearestResistance == {self.nearestResistance}"
        )
        addLogDetails(INFO, self.mainSchedulerText)
        while True:
            try:
                self.IndexLTP = getCurrentIndexValue(self.index_name)
                addLogDetails(INFO, self.IndexLTP)
                rounded_LTP = round(int(self.IndexLTP))
                if rounded_LTP >= self.nearestResistance or rounded_LTP <= self.nearestSupport or rounded_LTP in self.levels:
                    self.indexValueAfterTrendDecided = self.indexBaseValue
                    if rounded_LTP in self.levels:
                        self.pivotPoint = self.IndexLTP
                    elif rounded_LTP >= self.nearestResistance:
                        self.pivotPoint = self.nearestResistance
                    elif rounded_LTP <= self.nearestSupport:
                        self.pivotPoint = self.nearestSupport
                    updateIndexConfiguration(user_email=self.user_email, index=self.index_name,
                                             data={'stage': 'pivot_decided'})
                    addLogDetails(INFO, f"Index Name: {self.index_name} pivot Decided, User: {self.user_email}")
                    while True:
                        self.IndexLTP = getCurrentIndexValue(self.index_name)
                        addLogDetails(INFO, self.IndexLTP)
                        if self.IndexLTP >= int(self.pivotPoint) + self.index_trend_check:
                            self.CESetTargetAndStopLoss()
                            self.startCE()
                        elif self.IndexLTP <= int(self.pivotPoint) - self.index_trend_check:
                            self.PESetTargetAndStoploss()
                            self.startPE()
                        time.sleep(self.timeInterval)
            except Exception as e:
                addLogDetails(ERROR, f"exception in main while ----- {str(e)}")
            time.sleep(self.timeInterval)

    def CESetTargetAndStopLoss(self):
        try:
            self.indexValueAfterTrendDecided = self.IndexLTP - self.index_trend_check
            updateIndexConfiguration(user_email=self.user_email, index=self.index_name,
                                     data={'stage': f'Long :: {self.IndexLTP}'})
            self.stoplossExit = int(self.indexValueAfterTrendDecided) - self.index_trend_check
            self.exitConditions.append(self.stoplossExit)
            self.priceActionTarget = getTaregtForOrderFromList(self.levels, self.IndexLTP, "CE") - 5
            addLogDetails(INFO, f"Index Name: {self.index_name} CESetTargetAndStopLoss")
            addLogDetails(INFO, f"Index Name: {self.index_name} SL >> {self.stoplossExit}")
            addLogDetails(INFO, f"Index Name: {self.index_name} Target >> {self.priceActionTarget}")
        except Exception as e:
            addLogDetails(INFO, f"exception in CESetTargetAndStopLoss  -----  {e}")

    def PESetTargetAndStoploss(self):
        try:
            self.indexValueAfterTrendDecided = self.IndexLTP + self.index_trend_check
            updateIndexConfiguration(user_email=self.user_email, index=self.index_name,
                                     data={'stage': f'Short :: {self.IndexLTP}'})
            self.stoplossExit = int(self.indexValueAfterTrendDecided) + self.index_trend_check
            self.exitConditions.append(self.stoplossExit)
            self.priceActionTarget = getTaregtForOrderFromList(self.levels, self.IndexLTP, "PE") + 5
            addLogDetails(INFO, f"Index Name: {self.index_name} PESetTargetAndStoploss")
            addLogDetails(INFO, f"Index Name: {self.index_name} SL  >> {self.stoplossExit}")
            addLogDetails(INFO, f"Index Name: {self.index_name} Target >> {self.priceActionTarget}")
        except Exception as e:
            addLogDetails(ERROR, f"exception in PESetTargetAndStoploss  -----  {e}")

    def startCE(self):
        # self.isCEOrderPlaced = False
        while True:
            try:
                self.IndexLTP = getCurrentIndexValue(self.index_name)
                addLogDetails(INFO, str(self.IndexLTP))

                if not self.isCEOrderPlaced:
                    self.indexValueWhilePlacingOrder = self.IndexLTP
                    self.placeOrder("CE")
                    addLogDetails(INFO,
                                  f"Index Name: {self.index_name} User: {self.user_email} ExitConditions == {self.exitConditions}")

                if not self.isTrailStoplossPlaced:
                    self.placeStopLoss()

                if self.isTrailStoplossPlaced:
                    self.currentOptionPrice = self.BrokerObject.getLtpForPremium(self.optionDetails)
                    addLogDetails(INFO, f"isTrailStoplossPlaced {self.currentOptionPrice} {self.trailedSLPrice}")
                    if float(self.currentOptionPrice) <= self.trailedSLPrice:
                        self.exitBasedOnCondition(True, "Option price less than safeSL")
                        break

                if self.isOrderExited:
                    addLogDetails(INFO, "isOrderExited")
                    break

                if self.IndexLTP >= float(self.indexValueWhilePlacingOrder) + self.index_trailing:
                    addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} Into next trailing")
                    if self.exitConditions:
                        self.nextTrailing = int(max(self.exitConditions)) + self.index_trailing
                        self.exitConditions.append(self.nextTrailing)
                    else:
                        self.exitConditions.append(int(self.stoplossExit) + self.index_trailing)
                    self.indexValueWhilePlacingOrder += self.index_trailing
                    addLogDetails(INFO,
                                  f"Index Name: {self.index_name} User: {self.user_email} Adding new Value in exitConditions == {self.exitConditions}")

                if self.IndexLTP >= float(self.priceActionTarget):
                    addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} Into target")
                    self.exitBasedOnCondition(False, f"Target Reached - {self.IndexLTP}")
                    break

                elif self.IndexLTP < max(self.exitConditions):
                    addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} into exit at sl")
                    if self.IndexLTP <= self.stoplossExit:
                        addLogDetails(INFO,
                                      f"Index Name: {self.index_name} User: {self.user_email} Considering Stoploss taking inverse trade {self.stoplossExit}")
                        self.exitBasedOnCondition(False, f"Stoploss Hit - {self.IndexLTP}")
                        self.PESetTargetAndStoploss()
                        self.startPE()
                    else:
                        addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} into Trail Exit")
                        self.exitBasedOnCondition(False, f"Trailing Exit - {self.IndexLTP}")
                        break

                time.sleep(self.timeInterval)

            except Exception as e:
                addLogDetails(INFO,
                              f"Index Name: {self.index_name} User: {self.user_email} exception in startCE ----- {e}")

        self.initilize_price_action()

    def startPE(self):
        self.isPEOrderPlaced = False
        while True:
            try:
                self.IndexLTP = getCurrentIndexValue(self.index_name)
                addLogDetails(INFO, self.IndexLTP)

                if not self.isPEOrderPlaced:
                    self.indexValueWhilePlacingOrder = self.IndexLTP
                    self.placeOrder("PE")
                    addLogDetails(INFO,
                                  f"Index Name: {self.index_name} User: {self.user_email} ExitConditions == {self.exitConditions}")

                if not self.isTrailStoplossPlaced:
                    self.placeStopLoss()

                if self.isTrailStoplossPlaced:
                    addLogDetails(INFO, "isTrailStoplossPlaced")
                    self.currentOptionPrice = self.BrokerObject.getLtpForPremium(self.optionDetails)
                    if float(self.currentOptionPrice) <= self.trailedSLPrice:
                        self.exitBasedOnCondition(True, "Option price less than safeSL")
                        break

                if self.isOrderExited:
                    addLogDetails(INFO, "isOrderExited")
                    break

                if int(self.IndexLTP) <= int(self.indexValueWhilePlacingOrder) - self.index_trailing:
                    if self.exitConditions:
                        self.nextTrailing = int(min(self.exitConditions)) - self.index_trailing
                        self.exitConditions.append(self.nextTrailing)
                    else:
                        self.exitConditions.append(int(self.stoplossExit) - self.index_trailing)
                    self.indexValueWhilePlacingOrder -= self.index_trailing
                    addLogDetails(INFO,
                                  f"Index Name: {self.index_name} User: {self.user_email} Adding new Value in exitConditions == {self.exitConditions}")

                if self.IndexLTP <= self.priceActionTarget:
                    addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} into target")
                    self.exitBasedOnCondition(False, f"Target Reached - {self.IndexLTP}")
                    break

                elif self.IndexLTP > min(self.exitConditions):
                    addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} into exit at sl")
                    if self.IndexLTP >= self.stoplossExit:
                        addLogDetails(INFO,
                                      f"Index Name: {self.index_name} User: {self.user_email} Considering Stoploss taking inverse trade")
                        self.exitBasedOnCondition(False, f"Stoploss Hit - {self.IndexLTP}")
                        self.CESetTargetAndStopLoss()
                        self.startCE()
                    else:
                        self.exitBasedOnCondition(False, f"Trailing Exit - {self.IndexLTP}")
                        break

                time.sleep(self.timeInterval)

            except Exception as e:
                addLogDetails(ERROR, f"User: {self.user_email} exception in startPE ----- {e}")

        self.initilize_price_action()

    def exitBasedOnCondition(self, fromOptionPrice, reason):
        addLogDetails(INFO,
                      f"Index Name: {self.index_name} User: {self.user_email} Exit Based on condition called based on {reason}")

        try:
            if self.is_demo_enabled:
                self.revertDummyOrder(fromOptionPrice)
            else:
                if self.isStoplossPlaced and self.currentOrderID:
                    addLogDetails(INFO,
                                  f"Index Name: {self.index_name} User: {self.user_email} OrderId: {self.currentOrderID}")
                    self.revertOrderChecks(fromOptionPrice)

                    if self.BrokerObject.checkIfOrderExists(self.currentOrderID):
                        modify_order_details = {
                            EXCHANGE: NFO,
                            TRADING_SYMBOL: self.currentPremiumPlaced,
                            SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(self.currentPremiumPlaced),
                            ORDERID: self.currentExitOrderID,
                            ORDER_TYPE: MARKET,
                            QUANTITY: self.user_qty,
                            VARIETY: NORMAL,
                            DURATION: DAY
                        }
                        modify_order_response = self.BrokerObject.modifyOrder(modify_order_details)
                        addLogDetails(INFO,
                                      f"Index Name: {self.index_name} User: {self.user_email} ExitOrder: {modify_order_response}")
                        addLogDetails(INFO, "Order exited successfully")

                        self.optionExitPrice = self.BrokerObject.getPrice(self.currentOrderID)
                        addLogDetails(INFO,
                                      f"Index Name: {self.index_name} User: {self.user_email} Exit price = {self.optionExitPrice}")
                    else:
                        addLogDetails(INFO,
                                      f"Index Name: {self.index_name} User: {self.user_email} Current order not present")

            data = {
                USER_ID: self.user_email,
                SCRIPT_NAME: self.currentPremiumPlaced,
                QTY: self.qty,
                EXIT_PRICE: self.optionExitPrice,
                STATUS: ORDER_EXITED
            }
            addOrderBookDetails(data, False)
            addLogDetails(INFO,
                          f"Index Name: {self.index_name} User: {self.user_email} In {self.index_name} ExitConditions = {self.exitConditions}")

        except Exception as e:
            addLogDetails(ERROR, f"{self.index_name} exception in exitBasedOnCondition ----- {e}")

    def placeStopLoss(self):
        try:
            self.currentOptionPrice = self.BrokerObject.getLtpForPremium(self.optionDetails)

            if not self.isTrailStoplossPlaced and self.currentOptionPrice != CONNECTION_ERROR:
                current_option_price = float(self.currentOptionPrice)
                option_buy_price = float(self.optionBuyPrice)

                if current_option_price >= option_buy_price + self.targetforsafesl:
                    if self.is_demo_enabled:
                        self.trailedSLPrice = option_buy_price + self.safe_sl
                        addLogDetails(INFO,
                                      f"Index Name: {self.index_name} User: {self.user_email} Placed Safe SL = {self.trailedSLPrice}")
                    else:
                        addLogDetails(INFO,
                                      f"Index Name: {self.index_name} User: {self.user_email} Stoploss placed = {option_buy_price + self.safe_sl}")
                        price = int(option_buy_price) + self.safe_sl
                        trigger_price = price
                        modify_order_details = {
                            ORDERID: self.currentOrderID,
                            VARIETY: NORMAL,
                            EXCHANGE: NSE,
                            TRADING_SYMBOL: self.currentPremiumPlaced,
                            TRANSACTION_TYPE: SELL,
                            ORDER_TYPE: ORDER_TYPE_SL,
                            PRICE: price,
                            TRIGGER_PRICE: trigger_price,
                            PRODUCT_TYPE: INTRADAY,
                            DURATION: DAY,
                            QUANTITY: self.user_qty
                        }
                        self.currentOrderID = self.BrokerObject.modifyOrder(modify_order_details)
                        addLogDetails(INFO,
                                      f"Index Name: {self.index_name} User: {self.user_email} Sell order placed with target || Order ID = {self.currentOrderID}")

                    self.isTrailStoplossPlaced = True
                    addLogDetails(INFO,
                                  f"Index Name: {self.index_name} User: {self.user_email} Stoploss order placed: \t{self.currentPremiumPlaced} Stoploss price: \t{option_buy_price + self.safe_sl}")

                elif current_option_price <= option_buy_price - self.initialSL:
                    self.exitBasedOnCondition(True, "Option price less than Buy price")
                    self.isOrderExited = True

        except Exception as e:
            addLogDetails(ERROR, f"User: {self.user_email} {self.index_name} exception in placeStopLoss ----- {e}")

    def placeOrder(self, OrderType):
        try:
            self.indexValueWhilePlacingOrder = self.IndexLTP
            self.indexValueAfterTrendDecided = self.IndexLTP

            if OrderType == "CE":
                if not self.isCEOrderPlaced:
                    self.placeCallOption()
                else:
                    addLogDetails(INFO,
                                  f"Index Name: {self.index_name} User: {self.user_email} Order already placed: isCEOrderPlaced = {self.isCEOrderPlaced}")

            elif OrderType == "PE":
                if not self.isPEOrderPlaced:
                    self.placePutOption()
                else:
                    addLogDetails(INFO,
                                  f"Index Name: {self.index_name} User: {self.user_email} Order already placed: isPEOrderPlaced = {self.isPEOrderPlaced}")

        except Exception as e:
            addLogDetails(ERROR, f"User: {self.user_email} exception in placeOrder ----- {e}")

    def placeDummyOrder(self, orderType):
        try:
            addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} placeDummyOrder")

            # Simulate order response
            order_response = {'message': 'SUCCESS', 'data': {'orderid': 'dummy_id'}}

            self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
            self.optionBuyPrice = self.BrokerObject.getLtpForPremium(self.optionDetails)

            data = {
                USER_ID: self.user_email,
                SCRIPT_NAME: self.currentPremiumPlaced,
                QTY: self.qty,
                ENTRY_PRICE: self.optionBuyPrice,
                STATUS: ORDER_PLACED,
                STRATEGY: STRATEGY_HUNTER
            }

            addOrderBookDetails(data, True)

            if orderType == "CE":
                self.isCEOrderPlaced = True
            elif orderType == "PE":
                self.isPEOrderPlaced = True

            self.isStoplossPlaced = True
            self.currentOrderID = order_response['data']['orderid']

            return order_response

        except Exception as e:
            addLogDetails(ERROR, f"User: {self.user_email} exception in placeDummyOrder ----- {e}")

    def revertDummyOrder(self, fromOptionPrice):
        addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} revertDummyOrder")

        # Simulate order response
        order_response = {'message': 'SUCCESS', 'data': {'order_id': 'exit_dummy_id'}}

        self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
        exit_price = self.BrokerObject.getLtpForPremium(self.optionDetails)

        data = {
            USER_ID: self.user_email,
            SCRIPT_NAME: self.currentPremiumPlaced,
            QTY: self.qty,
            EXIT_PRICE: exit_price,
            STATUS: ORDER_EXITED
        }

        addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} {data}")
        addOrderBookDetails(data, False)

        self.revertOrderChecks(fromOptionPrice)

        return order_response

    def revertOrderChecks(self, fromOptionPrice):
        addLogDetails(INFO, "Into revertOrderChecks")
        if not fromOptionPrice:
            self.exitConditions = []
            self.isCEOrderPlaced = False
            self.isPEOrderPlaced = False
            self.isStoplossPlaced = False
            self.isTrailStoplossPlaced = False

    def placeCallOption(self):
        try:
            optionToBuy = f"{getTradingSymbol(self.index_name)}{self.BrokerObject.getCurrentAtm(self.index_name) - self.strike}CE"
            self.currentPremiumPlaced = optionToBuy

            addLogDetails(INFO,
                          f"Index Name: {self.index_name} User: {self.user_email} Current premium = {self.currentPremiumPlaced}")

            buy_order_details = {
                VARIETY: NORMAL,
                EXCHANGE: NFO,
                TRADING_SYMBOL: self.currentPremiumPlaced,
                SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(self.currentPremiumPlaced),
                TRANSACTION_TYPE: BUY,
                ORDER_TYPE: MARKET,
                PRODUCT_TYPE: INTRADAY,
                DURATION: DAY,
                QUANTITY: self.user_qty
            }

            addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} {buy_order_details}")

            if self.is_demo_enabled:
                order_response = self.placeDummyOrder("CE")
            else:
                order_response = self.BrokerObject.placeOrder(buy_order_details)
                addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} {order_response}")

                if order_response['message'] == 'SUCCESS':
                    uniqueorderid = order_response["data"]["uniqueorderid"]
                    order_details = self.BrokerObject.getOrderDetails(uniqueorderid)
                    addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} {order_details}")

                    self.optionBuyPrice = order_details["averageprice"]
                    data = {
                        USER_ID: self.user_email,
                        SCRIPT_NAME: self.currentPremiumPlaced,
                        QTY: self.qty,
                        ENTRY_PRICE: self.optionBuyPrice,
                        STATUS: ORDER_PLACED,
                        STRATEGY: STRATEGY_HUNTER
                    }

                    addOrderBookDetails(data, True)

                    price = int(self.optionBuyPrice) - 10
                    trigger_price = price
                    sell_order_details = {
                        VARIETY: STOPLOSS,
                        EXCHANGE: NFO,
                        TRADING_SYMBOL: self.currentPremiumPlaced,
                        SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(self.currentPremiumPlaced),
                        TRANSACTION_TYPE: SELL,
                        ORDER_TYPE: ORDER_TYPE_SL,
                        PRICE: price,
                        TRIGGER_PRICE: trigger_price,
                        PRODUCT_TYPE: INTRADAY,
                        DURATION: DAY,
                        QUANTITY: self.user_qty
                    }

                    addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} {sell_order_details}")

                    initial_sell_order = self.BrokerObject.placeOrder(sell_order_details)
                    addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} {initial_sell_order}")

                    self.currentOrderID = initial_sell_order["data"]["uniqueorderid"]
                    self.currentExitOrderID = initial_sell_order["data"]["orderid"]
                    self.isStoplossPlaced = True
                    self.isCEOrderPlaced = True

                    self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
                    addLogDetails(INFO,
                                  f"Index Name: {self.index_name} User: {self.user_email} BuyOrderPlaced: {self.currentPremiumPlaced} Entry price: {self.optionBuyPrice}")

                    updateIndexConfiguration(user_email=self.user_email, index=self.index_name,
                                             data={'stage': f'Long :: {self.IndexLTP}'})
                    addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} Long placed")

            addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} {order_response}")

        except Exception as e:
            addLogDetails(ERROR, f"User: {self.user_email} exception in placeCallOption ---- {e}")

    def placePutOption(self):
        try:
            optionToBuy = f"{getTradingSymbol(self.index_name)}{self.BrokerObject.getCurrentAtm(self.index_name) + self.strike}PE"
            self.currentPremiumPlaced = optionToBuy

            addLogDetails(INFO,
                          f"Index Name: {self.index_name} User: {self.user_email} Current premium = {self.currentPremiumPlaced}")

            buy_order_details = {
                VARIETY: NORMAL,
                EXCHANGE: NFO,
                TRADING_SYMBOL: self.currentPremiumPlaced,
                SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(self.currentPremiumPlaced),
                TRANSACTION_TYPE: BUY,
                ORDER_TYPE: MARKET,
                PRODUCT_TYPE: INTRADAY,
                DURATION: DAY,
                QUANTITY: self.user_qty
            }

            addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} {buy_order_details}")

            if self.is_demo_enabled:
                self.placeDummyOrder("PE")
            else:
                order_response = self.BrokerObject.placeOrder(buy_order_details)
                addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} {order_response}")

                if order_response[MESSAGE] == 'SUCCESS':
                    self.currentOrderID = order_response['data']['orderid']
                    uniqueorderid = order_response["data"]["uniqueorderid"]
                    self.optionBuyPrice = self.BrokerObject.getOrderDetails(uniqueorderid)["averageprice"]

                    self.isPEOrderPlaced = True
                    data = {
                        USER_ID: self.user_email,
                        SCRIPT_NAME: self.currentPremiumPlaced,
                        QTY: self.qty,
                        ENTRY_PRICE: self.optionBuyPrice,
                        STATUS: ORDER_PLACED,
                        STRATEGY: STRATEGY_HUNTER
                    }

                    addOrderBookDetails(data, True)

                    price = int(self.optionBuyPrice) - 10
                    trigger_price = price
                    sell_order_details = {
                        VARIETY: STOPLOSS,
                        EXCHANGE: NFO,
                        TRADING_SYMBOL: self.currentPremiumPlaced,
                        SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(self.currentPremiumPlaced),
                        TRANSACTION_TYPE: SELL,
                        ORDER_TYPE: ORDER_TYPE_SL,
                        PRICE: price,
                        TRIGGER_PRICE: trigger_price,
                        PRODUCT_TYPE: INTRADAY,
                        DURATION: DAY,
                        QUANTITY: self.user_qty
                    }

                    initial_sell_order = self.BrokerObject.placeOrder(sell_order_details)
                    addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} {initial_sell_order}")

                    self.currentOrderID = initial_sell_order["data"]["orderid"]
                    self.isStoplossPlaced = True

                    self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
                    addLogDetails(INFO,
                                  f"Index Name: {self.index_name} User: {self.user_email} BuyOrderPlaced: {self.currentPremiumPlaced} Entry price: {self.optionBuyPrice}")

                    updateIndexConfiguration(user_email=self.user_email, index=self.index_name,
                                             data={'stage': f'Short :: {self.IndexLTP}'})
                    addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} Short placed")

        except Exception as e:
            addLogDetails(ERROR, f"User: {self.user_email} exception in placePutOption ---- {e}")
