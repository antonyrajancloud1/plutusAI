from plutusAI.server.base import *
from plutusAI.server.constants import *
import time

class IndexPriceActionChecker:
    def __init__(self, index_name, user_email, BrokerObject, config):
        try:
            self.index_name = index_name
            self.user_email = user_email
            self.BrokerObject = BrokerObject

            # Convert string values to correct types
            levels_raw = config.get("levels", "")
            self.levels = list(map(int, levels_raw.split(','))) if isinstance(levels_raw, str) else levels_raw
            self.strike = int(config.get("strike", 0))
            self.index_trend_check = int(config.get("trend_check_points", 20))
            self.user_qty = int(config.get("user_qty", 75))
            self.is_demo_enabled = self.BrokerObject.is_demo_enabled
            self.is_place_sl_required = config.get("is_place_sl_required", False)
            self.initialSL = int(config.get("initialSL", 10))
            self.wait_for_candle_confirmation = config.get("next_candle_confirmation", False)

            self.use_levels = config.get("use_levels", False)
            self.use_stoploss = self.is_place_sl_required

            self.isCEOrderPlaced = False
            self.isPEOrderPlaced = False
            self.isStoplossPlaced = False
            self.pivotPoint = None
            self.isPivotDecided=False
            self.indexBaseValue = None
            self.IndexLTP = None
            self.currentOrderID = None
            self.currentExitOrderID = None
            self.optionDetails = None
            self.currentPremiumPlaced = None
            self.optionBuyPrice = None
            self.exitConditions = []
            self.indexValueWhilePlacingOrder = None
            self.indexValueAfterTrendDecided = None
            self.stoplossExit = None
            self.priceActionTarget = None
            self.optionExitPrice= None
            addLogDetails(INFO, "[__init__] Initialized IndexPriceActionChecker")
            updateIndexConfiguration(user_email=self.user_email, index=self.index_name, data={'status': 'running'})
        except Exception as e:
            addLogDetails(ERROR, f"[__init__] Error: {e}")

    def updateIndex(self):
        try:
            self.IndexLTP = round(getCurrentIndexValue(self.index_name))
            print(self.IndexLTP)
            addLogDetails(INFO, f"[updateIndex] Updated IndexLTP: {self.IndexLTP}")
        except Exception as e:
            addLogDetails(ERROR, f"[updateIndex] Error: {e}")

    def checkAndSetPivot(self):
        try:
            self.updateIndex()
            self.indexBaseValue = self.IndexLTP

            if self.use_levels:
                self.nearestSupport = getTaregtForOrderFromList(self.levels, self.indexBaseValue, "PE")
                self.nearestResistance = getTaregtForOrderFromList(self.levels, self.indexBaseValue, "CE")

                at_level = self.IndexLTP in self.levels
                near_support = self.IndexLTP <= self.nearestSupport
                near_resistance = self.IndexLTP >= self.nearestResistance

                if at_level or near_support or near_resistance:
                    self.pivotPoint = (
                        self.IndexLTP if at_level else
                        self.nearestResistance if near_resistance else
                        self.nearestSupport
                    )
            else:
                self.pivotPoint = self.IndexLTP

            if self.pivotPoint:
                self.isPivotDecided = True
                self._logPivotDecision()

        except Exception as e:
            addLogDetails(ERROR, f"[checkAndSetPivot] Error: {e}")

    def _logPivotDecision(self):
        updateIndexConfiguration(
            user_email=self.user_email,
            index=self.index_name,
            data={'status': f'Pivot Decided : {self.pivotPoint}'}
        )
        addLogDetails(INFO, f"[checkAndSetPivot] Pivot set to {self.pivotPoint}")

    # def evaluatePriceAction(self):
    #     try:
    #         while True:
    #             time.sleep(1)
    #             if not self.isPivotDecided:
    #                 self.checkAndSetPivot()
    #             elif self.isPivotDecided:
    #                 self.updateIndex()
    #                 if self.IndexLTP >= self.pivotPoint + self.index_trend_check:
    #                     self.startCE()
    #                 elif self.IndexLTP <= self.pivotPoint - self.index_trend_check:
    #                     self.startPE()
    #                 else:
    #                     addLogDetails(INFO, f"[evaluatePriceAction] Index {self.index_name} holding near pivot {self.pivotPoint}, no action taken.")
    #     except Exception as e:
    #         addLogDetails(ERROR, f"[evaluatePriceAction] Error: {e}")
    def evaluatePriceAction(self):
        try:
            current_order = None  # 'CE' or 'PE'
            entry_price = None
            stop_loss = None

            while True:
                time.sleep(1)
                if not self.isPivotDecided:
                    self.checkAndSetPivot()
                else:
                    self.updateIndex()

                    # No active order yet
                    if current_order is None:
                        if self.IndexLTP >= self.pivotPoint + self.index_trend_check:
                            current_order = 'CE'
                            entry_price = self.IndexLTP
                            stop_loss = entry_price - self.index_trend_check
                            self.startCE()
                            addLogDetails(INFO,
                                          f"[evaluatePriceAction] CE started at {entry_price} with SL {stop_loss}")

                        elif self.IndexLTP <= self.pivotPoint - self.index_trend_check:
                            current_order = 'PE'
                            entry_price = self.IndexLTP
                            stop_loss = entry_price + self.index_trend_check
                            self.startPE()
                            addLogDetails(INFO,
                                          f"[evaluatePriceAction] PE started at {entry_price} with SL {stop_loss}")

                    # CE active
                    elif current_order == 'CE':
                        if self.IndexLTP >= entry_price + self.index_trend_check:
                            entry_price = self.IndexLTP
                            stop_loss = entry_price - self.index_trend_check
                            addLogDetails(INFO,
                                          f"[evaluatePriceAction] CE SL trailed to: {stop_loss} | New Entry Base: {entry_price}")

                        elif self.IndexLTP <= stop_loss:
                            addLogDetails(INFO, f"[evaluatePriceAction] CE SL hit at {self.IndexLTP}, switching to PE")
                            self.exitBasedOnCondition(self.IndexLTP, reason="SL hit")
                            current_order = 'PE'
                            entry_price = self.IndexLTP
                            stop_loss = entry_price + self.index_trend_check
                            self.startPE()
                            addLogDetails(INFO,
                                          f"[evaluatePriceAction] PE started at {entry_price} with SL {stop_loss}")

                    # PE active
                    elif current_order == 'PE':
                        if self.IndexLTP <= entry_price - self.index_trend_check:
                            entry_price = self.IndexLTP
                            stop_loss = entry_price + self.index_trend_check
                            addLogDetails(INFO,
                                          f"[evaluatePriceAction] PE SL trailed to: {stop_loss} | New Entry Base: {entry_price}")

                        elif self.IndexLTP >= stop_loss:
                            addLogDetails(INFO, f"[evaluatePriceAction] PE SL hit at {self.IndexLTP}, switching to CE")
                            self.exitBasedOnCondition(self.IndexLTP, reason="SL hit")
                            current_order = 'CE'
                            entry_price = self.IndexLTP
                            stop_loss = entry_price - self.index_trend_check
                            self.startCE()
                            addLogDetails(INFO,
                                          f"[evaluatePriceAction] CE started at {entry_price} with SL {stop_loss}")
        except Exception as e:
            addLogDetails(ERROR, f"[evaluatePriceAction] Error: {e}")

    def startCE(self):
        try:
            if not self.isCEOrderPlaced:
                print("CE not placed")
                self.resetPEFlag()
                self.CESetTargetAndStopLoss()
                self.placeOrder("CE",self.strike)
            else:
                print("CE already placed")
        except Exception as e:
            addLogDetails(ERROR, f"[startCE] Error: {e}")

    def startPE(self):
        try:
            if not self.isPEOrderPlaced:
                self.resetCEFlag()
                self.PESetTargetAndStoploss()
                self.placeOrder("PE",-self.strike)
            else:
                print("PE is already placed")
        except Exception as e:
            addLogDetails(ERROR, f"[startPE] Error: {e}")

    def resetCEFlag(self):
        try:
            self.isCEOrderPlaced = False
            addLogDetails(INFO, "[resetCEFlag] CE order flag reset")
        except Exception as e:
            addLogDetails(ERROR, f"[resetCEFlag] Error: {e}")

    def resetPEFlag(self):
        try:
            self.isPEOrderPlaced = False
            addLogDetails(INFO, "[resetPEFlag] PE order flag reset")
        except Exception as e:
            addLogDetails(ERROR, f"[resetPEFlag] Error: {e}")

    def CESetTargetAndStopLoss(self):
        try:
            if self.use_levels:
                self.indexValueAfterTrendDecided = self.IndexLTP - self.index_trend_check
                self.stoplossExit = self.indexValueAfterTrendDecided - self.index_trend_check
                self.exitConditions.append(self.stoplossExit)
                self.priceActionTarget = getTaregtForOrderFromList(self.levels, self.IndexLTP, "CE") - 5
                updateIndexConfiguration(user_email=self.user_email, index=self.index_name, data={'status': 'Long :: ' + str(self.IndexLTP)})
                addLogDetails(INFO, f"[CESetTargetAndStopLoss] Index: {self.index_name}, SL: {self.stoplossExit}, Target: {self.priceActionTarget}")
        except Exception as e:
            addLogDetails(ERROR, f"[CESetTargetAndStopLoss] Error: {e}")

    def PESetTargetAndStoploss(self):
        try:
            if self.use_levels:
                self.indexValueAfterTrendDecided = self.IndexLTP + self.index_trend_check
                self.stoplossExit = self.indexValueAfterTrendDecided + self.index_trend_check
                self.exitConditions.append(self.stoplossExit)
                self.priceActionTarget = getTaregtForOrderFromList(self.levels, self.IndexLTP, "PE") + 5
                updateIndexConfiguration(user_email=self.user_email, index=self.index_name, data={'status': 'Short :: ' + str(self.IndexLTP)})
                addLogDetails(INFO, f"[PESetTargetAndStoploss] Index: {self.index_name}, SL: {self.stoplossExit}, Target: {self.priceActionTarget}")
        except Exception as e:
            addLogDetails(ERROR, f"[PESetTargetAndStoploss] Error: {e}")

    def placeOrder(self, direction: str, strike_offset: int):
        try:
            suffix = self.getSuffix(direction)
            atm_strike = self.BrokerObject.getCurrentAtm(self.index_name)
            optionToBuy = f"{getTradingSymbol(self.index_name)}{atm_strike + strike_offset}{suffix}"
            self.currentPremiumPlaced = optionToBuy

            order_details = self._prepareOrderDetails(optionToBuy, BUY, MARKET)
            addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} {order_details}")

            order_response = self.placeDummyOrder(direction) if self.is_demo_enabled else self.BrokerObject.placeOrder(
                order_details)

            if order_response.get("message") == "SUCCESS":
                self._handleSuccessfulOrder(order_response, optionToBuy, direction)
        except Exception as e:
            addLogDetails(ERROR, f"User: {self.user_email} exception in place{direction} ---- {e}")

    def _prepareOrderDetails(self, symbol: str, txn_type: str, order_type: str, price=None, trigger_price=None):
        details = {
            VARIETY: NORMAL if order_type == MARKET else STOPLOSS,
            EXCHANGE: NFO,
            TRADING_SYMBOL: symbol,
            SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(symbol),
            TRANSACTION_TYPE: txn_type,
            ORDER_TYPE: order_type,
            PRODUCT_TYPE: INTRADAY,
            DURATION: DAY,
            QUANTITY: self.user_qty
        }
        if price:
            details[PRICE] = price
        if trigger_price:
            details[TRIGGER_PRICE] = trigger_price
        return details

    def _handleSuccessfulOrder(self, response, option_symbol, direction):
        data = response["data"]
        self.currentOrderID = data.get("uniqueorderid", data.get("orderid"))
        self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, option_symbol)
        self.optionBuyPrice = self.BrokerObject.getLtpForPremium(self.optionDetails)

        order_data = {
            USER_ID: self.user_email,
            SCRIPT_NAME: option_symbol,
            QTY: self.user_qty,
            ENTRY_PRICE: self.optionBuyPrice,
            STATUS: ORDER_PLACED,
            STRATEGY: STRATEGY_HUNTER,
            INDEX_NAME: self.index_name
        }

        if not self.is_demo_enabled:
            addOrderBookDetails(order_data, True)

            if self.is_place_sl_required:
                sl_price = float(self.optionBuyPrice) - self.initialSL
                sl_order_details = self._prepareOrderDetails(option_symbol, SELL, ORDER_TYPE_SL, price=sl_price,
                                                             trigger_price=sl_price)
                sl_order = self.BrokerObject.placeOrder(sl_order_details)
                self.currentExitOrderID = sl_order["data"]["orderid"]
                self.isStoplossPlaced = True

        if direction == "CE":
            self.isCEOrderPlaced = True
            status_str = f"Long :: {self.IndexLTP}"
        else:
            self.isPEOrderPlaced = True
            status_str = f"Short :: {self.IndexLTP}"

        updateIndexConfiguration(self.user_email, self.index_name, {"status": status_str})

    def getSuffix(self, direction):
        return "CE" if direction == "CE" else "PE"

    def placeDummyOrder(self, orderType):
        try:
            addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} placeDummyOrder")
            order_id = f"dummy_{int(time.time())}"
            order_response = {'message': 'SUCCESS', 'data': {'orderid': order_id}}

            self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
            self.optionBuyPrice = self.BrokerObject.getLtpForPremium(self.optionDetails)
            addLogDetails(INFO, f"Simulated LTP for {self.currentPremiumPlaced}: {self.optionBuyPrice}")

            data = {
                USER_ID: self.user_email, SCRIPT_NAME: self.currentPremiumPlaced,
                QTY: self.user_qty, ENTRY_PRICE: self.optionBuyPrice,
                STATUS: ORDER_PLACED, STRATEGY: STRATEGY_HUNTER, INDEX_NAME: self.index_name
            }

            if orderType == "CE":
                self.isCEOrderPlaced = True
            elif orderType == "PE":
                self.isPEOrderPlaced = True

            self.currentOrderID = order_id
            self.currentExitOrderID = f"{order_id}_SL"
            self.isStoplossPlaced = True
            addOrderBookDetails(data, True)
            print("DummY Order Placed")
            return order_response

        except Exception as e:
            addLogDetails(ERROR, f"User: {self.user_email} exception in placeDummyOrder ----- {e}")
            return {'message': 'ERROR', 'error': str(e)}

    def exitBasedOnCondition(self, fromOptionPrice, reason):
        addLogDetails(INFO,
                      f"Index Name: {self.index_name} | User: {self.user_email} | Exit triggered due to: {reason}")
        try:
            if self.is_demo_enabled:
                self.revertDummyOrder(fromOptionPrice)
            else:

                addLogDetails(INFO,
                              f"Index Name: {self.index_name} | User: {self.user_email} | OrderID: {self.currentOrderID}")
                # self.revertOrderChecks(fromOptionPrice)
                if self.is_place_sl_required  and self.isStoplossPlaced and self.currentOrderID:
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
                                      f"Index Name: {self.index_name} | User: {self.user_email} | ExitOrder: {modify_order_response}")
                        addLogDetails(INFO, "Order exited successfully")

                        # Try to get actual exit price
                        self.optionExitPrice = self.BrokerObject.getPrice(self.currentOrderID)
                        if not self.optionExitPrice:
                            self.optionExitPrice = fromOptionPrice  # Fallback
                        addLogDetails(INFO,
                                      f"Index Name: {self.index_name} | User: {self.user_email} | Exit price = {self.optionExitPrice}")

                    else:
                        addLogDetails(INFO,
                                      f"Index Name: {self.index_name} | User: {self.user_email} | Order no longer exists")
                else:
                    order_details = self._prepareOrderDetails(self.currentPremiumPlaced, SELL, MARKET)
                    addLogDetails(INFO,
                                  f"Index Name: {self.index_name} User: {self.user_email} {order_details}")

                    order_response =  self.BrokerObject.placeOrder(order_details)
                    print(order_response)
                    self.optionExitPrice = self.BrokerObject.getLtpForPremium(self.optionDetails)
                    data = {USER_ID: self.user_email, SCRIPT_NAME: self.currentPremiumPlaced,
                            QTY: self.user_qty,
                            EXIT_PRICE: self.BrokerObject.getLtpForPremium(self.optionDetails),
                            STATUS: ORDER_EXITED}
                    addLogDetails(INFO,
                                  "Index Name: " + self.index_name + " User :" + self.user_email + " " + str(
                                      data))
                    addOrderBookDetails(data, False)

            # Record exit in OrderBook
            data = {
                USER_ID: self.user_email,
                SCRIPT_NAME: self.currentPremiumPlaced,
                QTY: self.user_qty,
                EXIT_PRICE: self.optionExitPrice,
                STATUS: ORDER_EXITED
            }
            addOrderBookDetails(data, False)

            # Reset strategy-related state here if needed
            self.currentOrderID = ""
            self.currentExitOrderID = ""
            self.optionExitPrice = None
            self.isStoplossPlaced = False
            self.entry_price = None
            self.stop_loss = None
            self.current_order = None

            addLogDetails(INFO,
                          f"Index Name: {self.index_name} | User: {self.user_email} | Exit conditions: {self.exitConditions}")

        except Exception as e:
            addLogDetails(ERROR, f"{self.index_name} | Exception in exitBasedOnCondition: {e}")

    def revertDummyOrder(self, fromOptionPrice):
        addLogDetails(INFO, "Index Name: " + self.index_name + " User :" + self.user_email + " revertDummyOrder")
        order_response = {'message': 'SUCCESS', 'data': {'order_id': 'exit_dummy_id'}}
        self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, self.currentPremiumPlaced)
        data = {USER_ID: self.user_email, SCRIPT_NAME: self.currentPremiumPlaced, QTY: self.user_qty,
                EXIT_PRICE: self.BrokerObject.getLtpForPremium(self.optionDetails), STATUS: ORDER_EXITED}
        addLogDetails(INFO, "Index Name: " + self.index_name + " User :" + self.user_email + " " + str(data))
        addOrderBookDetails(data, False)
        # self.revertOrderChecks(fromOptionPrice)
        return order_response
