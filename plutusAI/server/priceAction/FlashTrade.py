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
            self.index_trend_check = int(config.get("index_trend_check", 50))
            self.user_qty = int(config.get("user_qty", 50))
            self.is_demo_enabled = config.get("is_demo_enabled", False)
            self.is_place_sl_required = config.get("is_place_sl_required", True)
            self.initialSL = int(config.get("initialSL", 10))
            self.wait_for_candle_confirmation = config.get("next_candle_confirmation", False)

            self.use_levels = config.get("use_levels", False)
            self.use_stoploss = self.is_place_sl_required

            self.isCEOrderPlaced = False
            self.isPEOrderPlaced = False
            self.isStoplossPlaced = False
            self.pivotPoint = None
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

            addLogDetails(INFO, "[__init__] Initialized IndexPriceActionChecker")
            updateIndexConfiguration(user_email=self.user_email, index=self.index_name, data={'status': 'running'})
        except Exception as e:
            addLogDetails(ERROR, f"[__init__] Error: {e}")

    def updateIndex(self):
        try:
            self.IndexLTP = round(getCurrentIndexValue(self.index_name))
            addLogDetails(INFO, f"[updateIndex] Updated IndexLTP: {self.IndexLTP}")
        except Exception as e:
            addLogDetails(ERROR, f"[updateIndex] Error: {e}")

    def checkAndSetPivot(self):
        try:
            while True:
                self.updateIndex()
                self.indexBaseValue = self.IndexLTP
                if self.use_levels:
                    self.nearestSupport = getTaregtForOrderFromList(self.levels, self.indexBaseValue, "PE")
                    self.nearestResistance = getTaregtForOrderFromList(self.levels, self.indexBaseValue, "CE")

                    if (
                        self.IndexLTP in self.levels or
                        self.IndexLTP <= self.nearestSupport or
                        self.IndexLTP >= self.nearestResistance
                    ):
                        self.pivotPoint = (
                            self.IndexLTP if self.IndexLTP in self.levels else
                            self.nearestResistance if self.IndexLTP >= self.nearestResistance else
                            self.nearestSupport
                        )
                else:
                    self.pivotPoint = self.IndexLTP

                if self.pivotPoint:
                    updateIndexConfiguration(
                        user_email=self.user_email,
                        index=self.index_name,
                        data={'status': f'Pivot Decided : {self.pivotPoint}'}
                    )
                    addLogDetails(INFO, f"[checkAndSetPivot] Pivot set to {self.pivotPoint}")
                    break

        except Exception as e:
            addLogDetails(ERROR, f"[checkAndSetPivot] Error: {e}")

    def evaluatePriceAction(self):
        try:
            if not self.pivotPoint:
                self.checkAndSetPivot()
                return

            self.updateIndex()
            if self.IndexLTP >= self.pivotPoint + self.index_trend_check:
                self.startCE()
            elif self.IndexLTP <= self.pivotPoint - self.index_trend_check:
                self.startPE()
            else:
                addLogDetails(INFO, f"[evaluatePriceAction] Index {self.index_name} holding near pivot {self.pivotPoint}, no action taken.")
        except Exception as e:
            addLogDetails(ERROR, f"[evaluatePriceAction] Error: {e}")

    def startCE(self):
        try:
            if self.isStoplossPlaced:
                addLogDetails(INFO, f"[startCE] Stoploss already placed. Blocking CE entry.")
                return
            self.resetPEFlag()
            self.CESetTargetAndStopLoss()
            self.placeOrder("CE")
        except Exception as e:
            addLogDetails(ERROR, f"[startCE] Error: {e}")

    def startPE(self):
        try:
            if self.isStoplossPlaced:
                addLogDetails(INFO, f"[startPE] Stoploss already placed. Blocking PE entry.")
                return
            self.resetCEFlag()
            self.PESetTargetAndStoploss()
            self.placeOrder("PE")
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
            optionToBuy = getTradingSymbol(self.index_name) + str(
                self.BrokerObject.getCurrentAtm(self.index_name) + strike_offset) + suffix
            self.currentPremiumPlaced = optionToBuy

            buy_order_details = {
                VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: optionToBuy,
                SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(optionToBuy),
                TRANSACTION_TYPE: BUY, ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY,
                DURATION: DAY, QUANTITY: self.user_qty
            }

            addLogDetails(INFO, f"Index Name: {self.index_name} User: {self.user_email} {buy_order_details}")

            if self.is_demo_enabled:
                order_response = self.placeDummyOrder(direction)
            else:
                order_response = self.BrokerObject.placeOrder(buy_order_details)

            if order_response.get("message") == "SUCCESS":
                uniqueorderid = order_response["data"].get("uniqueorderid", order_response["data"].get("orderid"))
                self.currentOrderID = uniqueorderid
                self.optionDetails = self.BrokerObject.getCurrentPremiumDetails(NFO, optionToBuy)
                self.optionBuyPrice = self.BrokerObject.getLtpForPremium(self.optionDetails)

                data = {
                    USER_ID: self.user_email, SCRIPT_NAME: optionToBuy, QTY: self.user_qty,
                    ENTRY_PRICE: self.optionBuyPrice, STATUS: ORDER_PLACED,
                    STRATEGY: STRATEGY_HUNTER, INDEX_NAME: self.index_name
                }
                addOrderBookDetails(data, True)

                if self.is_place_sl_required:
                    sl_price = int(self.optionBuyPrice) - self.initialSL
                    sl_order_details = {
                        VARIETY: STOPLOSS, EXCHANGE: NFO, TRADING_SYMBOL: optionToBuy,
                        SYMBOL_TOKEN: self.BrokerObject.getTokenForSymbol(optionToBuy),
                        TRANSACTION_TYPE: SELL, ORDER_TYPE: ORDER_TYPE_SL,
                        PRICE: sl_price, TRIGGER_PRICE: sl_price,
                        PRODUCT_TYPE: INTRADAY, DURATION: DAY,
                        QUANTITY: self.user_qty
                    }
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

        except Exception as e:
            addLogDetails(ERROR, f"User: {self.user_email} exception in place{direction}Option ---- {e}")

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
            addOrderBookDetails(data, True)

            if orderType == "CE":
                self.isCEOrderPlaced = True
            elif orderType == "PE":
                self.isPEOrderPlaced = True

            self.currentOrderID = order_id
            self.currentExitOrderID = f"{order_id}_SL"
            self.isStoplossPlaced = True

            return order_response

        except Exception as e:
            addLogDetails(ERROR, f"User: {self.user_email} exception in placeDummyOrder ----- {e}")
            return {'message': 'ERROR', 'error': str(e)}

