from plutusAI.server.broker.Broker import Broker
from plutusAI.server.priceAction.priceActionScalper import *


class FlashTrade:

    def __init__(self, user_email, index, index_group):
        try:
            self.strategy = STRATEGY_FLASH
            self.user_email = user_email
            self.index_name = index
            self.index_group = index_group
            self.init_default_values()
            self.user_data = FlashDetails.objects.filter(user_id=user_email, index_name=index)
            self.index_data = IndexDetails.objects.filter(index_name=index)

            self.index_data = list(self.index_data.values())
            self.flash_data = list(self.user_data.values())
            addLogDetails(INFO, "before broker object")
            self.broker_object = Broker(self.user_email, self.index_group).BrokerObject
            self.is_demo_enabled = self.broker_object.is_demo_enabled
            addLogDetails(INFO, "After broker object")

            if self.broker_object.checkProfile()[MESSAGE] == "SUCCESS":
                addLogDetails(INFO, "Into broker object")
                if len(self.flash_data) > 0:
                    self.flash_data = self.flash_data[0]
                    self.index_trend_check = float(self.flash_data[TREND_CHECK_POINTS])
                    self.index_trailing = float(self.flash_data[TRAILING_POINTS])
                    self.lots = int(self.flash_data[LOTS])
                    self.qty = int(self.index_data[0][QTY])
                    self.strike = int(self.flash_data[STRIKE])
                    self.user_qty = self.qty * self.lots
                    self.max_profit = int(self.flash_data[MAX_PROFIT])
                    self.max_loss = int(self.flash_data[MAX_LOSS])
                    self.average_points = int(self.flash_data["average_points"])
                    self.time_interval = 1
                    self.initialize_price_action()
            else:
                updateFlashConfiguration(user_email=self.user_email, index=self.index_name, data=STAGE_BROKER_NOT_PRESENT)
                addLogDetails(ERROR, "Flash Details not present")

        except Exception as e:
            addLogDetails(ERROR, f"FlashTrade init error: {e}")

    def init_default_values(self):
        self.is_order_exited = False
        self.index_ltp = 0
        self.isCEOrderPlaced = False
        self.isPEOrderPlaced = False
        self.index_base_value = 0
        self.indexValueWhilePlacingOrder = 0
        self.currentOrders = []
        self.ce_averaged = False
        self.pe_averaged = False
        self.orderCount = 0
        self.orderedQty = 0

    def initialize_price_action(self):
        addLogDetails(INFO, "initialize_price_action")
        updateFlashConfiguration(user_email=self.user_email, index=self.index_name, data=STAGE_STARTED)
        self.index_base_value = getCurrentIndexValue(self.index_name)

        while True:
            try:
                self.index_ltp = float(getCurrentIndexValue(self.index_name))
                addLogDetails(INFO, f"{self.index_name} LTP: {self.index_ltp}")
                self.PECondition = self.index_ltp < float(self.index_base_value) - float(self.index_trend_check)
                self.CECondition = self.index_ltp > float(self.index_base_value) + float(self.index_trend_check)
                if self.CECondition:
                    self.start_ce()
                elif self.PECondition:
                    self.start_pe()
                time.sleep(self.time_interval)
            except Exception as e:
                addLogDetails(ERROR, f"Exception in FlashTrade loop: {e}")
                time.sleep(self.time_interval)

    def start_ce(self):
        try:
            while True:
                time.sleep(self.time_interval)
                self.PECondition = self.index_ltp < float(self.index_base_value) - float(self.index_trend_check)
                self.CECondition = self.index_ltp > float(self.index_base_value) + float(self.index_trend_check)
                self.index_ltp = float(getCurrentIndexValue(self.index_name))

                if not self.isCEOrderPlaced:
                    addLogDetails(INFO, "Placing CE order...")
                    self.exitOrders()
                    self.isCEOrderPlaced = True
                    self.isPEOrderPlaced = False
                    self.ce_averaged = False
                    self.orderCount = 1
                    self.orderedQty = self.user_qty * self.orderCount
                    self.indexValueWhilePlacingOrder = self.index_ltp

                    strike_price = self.broker_object.getCurrentAtm(self.index_name) - self.strike
                    optionToBuy = f"{getTradingSymbol(self.index_name)}{strike_price}CE"
                    self.currentOrders.append(optionToBuy)

                    addLogDetails(INFO, f"✅ CE Order Placed: {optionToBuy}")
                    addLogDetails(INFO, f"🟢 Current Orders: {self.currentOrders}")
                    addLogDetails(INFO, f"📦 Order Count: {self.orderCount}, Ordered Qty: {self.orderedQty}")

                elif self.isCEOrderPlaced:
                    trigger = self.indexValueWhilePlacingOrder - self.average_points
                    ltp = self.index_ltp
                    addLogDetails(INFO, f"nifty LTP: {ltp}")
                    addLogDetails(INFO, f"Trigger for averaging: {trigger}, Base value: {self.index_base_value}")
                    if trigger >= ltp >= self.index_base_value and not self.ce_averaged:
                        self.ce_averaged = True
                        self.orderCount += 1
                        self.orderedQty = self.user_qty * self.orderCount
                        self.currentOrders.append(self.currentOrders[0])  # Add same order for averaging
                        addLogDetails(INFO, f"✅ Averaging CE: Order Count = {self.orderCount}, Qty = {self.orderedQty}")
                        addLogDetails(INFO, f"🟢 Updated Orders: {self.currentOrders}")
                elif self.PECondition:
                    addLogDetails(INFO, "Switch")
                    break

        except Exception as e:
            addLogDetails(ERROR, f"❌ Error in start_ce: {str(e)}")

    def start_pe(self):
        try:
            while True:
                self.PECondition = self.index_ltp < float(self.index_base_value) - float(self.index_trend_check)
                self.CECondition = self.index_ltp > float(self.index_base_value) + float(self.index_trend_check)
                time.sleep(self.time_interval)
                self.index_ltp = float(getCurrentIndexValue(self.index_name))

                if not self.isPEOrderPlaced:
                    addLogDetails(INFO, "Placing PE order...")
                    self.exitOrders()
                    self.isPEOrderPlaced = True
                    self.isCEOrderPlaced = False
                    self.pe_averaged = False
                    self.orderCount = 1
                    self.orderedQty = self.user_qty * self.orderCount
                    self.indexValueWhilePlacingOrder = self.index_ltp

                    strike_price = self.broker_object.getCurrentAtm(self.index_name) + self.strike
                    optionToBuy = f"{getTradingSymbol(self.index_name)}{strike_price}PE"
                    self.currentOrders.append(optionToBuy)

                    addLogDetails(INFO, f"✅ PE Order Placed: {optionToBuy}")
                    addLogDetails(INFO, f"🟢 Current Orders: {self.currentOrders}")
                    addLogDetails(INFO, f"📦 Order Count: {self.orderCount}, Ordered Qty: {self.orderedQty}")

                elif self.isPEOrderPlaced:
                    trigger = self.indexValueWhilePlacingOrder + self.average_points
                    ltp = self.index_ltp
                    addLogDetails(INFO, f"nifty LTP: {ltp}")
                    addLogDetails(INFO, f"Trigger for averaging: {trigger}, Base value: {self.index_base_value}")
                    if trigger <= ltp <= self.index_base_value and not self.pe_averaged:
                        self.pe_averaged = True
                        self.orderCount += 1
                        self.orderedQty = self.user_qty * self.orderCount
                        self.currentOrders.append(self.currentOrders[0])  # Add same order for averaging
                        addLogDetails(INFO, f"✅ Averaging PE: Order Count = {self.orderCount}, Qty = {self.orderedQty}")
                        addLogDetails(INFO, f"🟢 Updated Orders: {self.currentOrders}")
                elif self.CECondition:
                    addLogDetails(INFO, "Switch")
                    break

        except Exception as e:
            addLogDetails(ERROR, f"❌ Error in start_pe: {str(e)}")

    def exitOrders(self):
        self.currentOrders = []
        self.orderCount = 0
        self.orderedQty = 0
        print("🚪 Exiting all previous orders")
