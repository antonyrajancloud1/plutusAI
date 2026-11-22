from plutusAI.server.base import *
from plutusAI.server.constants import *
from concurrent.futures import ThreadPoolExecutor
import time

class IndexPriceActionChecker:
    def __init__(self, index_name, user_email, BrokerObject, config):
        try:
            self.index_name = index_name
            self.user_email = user_email
            self.BrokerObject = BrokerObject

            # Convert string values to correct types
            levels_raw = config.get("levels") or ""
            self.levels = (
                [int(level.strip()) for level in levels_raw.split(",") if level.strip()]
                if isinstance(levels_raw, str)
                else levels_raw
            )
            self.strike = int(config.get("strike", 0))
            self.index_trend_check = int(config.get("trend_check_points", 20))
            self.user_qty = int(config.get("user_qty", 75))
            self.is_demo_enabled = self.BrokerObject.is_demo_enabled
            self.is_place_sl_required = self._as_bool(config.get("is_place_sl_required", False))
            self.initialSL = float(config.get("initialSL", config.get("initial_sl", 10)))
            self.wait_for_candle_confirmation = config.get("next_candle_confirmation", False)

            self.use_levels = self._as_bool(config.get("use_levels", False))
            self.use_stoploss = self.is_place_sl_required

            # Premium-pair settings.  Defaults deliberately require several
            # confirming ticks so a single noisy option tick cannot open/close
            # a position.  They may be overridden per user configuration.
            self.monitor_interval_seconds = float(config.get("monitor_interval_seconds", 1))
            self.entry_confirmation_ticks = max(2, int(config.get("entry_confirmation_ticks", 3)))
            self.exit_confirmation_ticks = max(2, int(config.get("exit_confirmation_ticks", 3)))
            self.trailing_exit_confirmation_ticks = max(
                2, int(config.get("trailing_exit_confirmation_ticks", 2))
            )
            self.minimum_hold_ticks = max(0, int(config.get("minimum_hold_ticks", 3)))
            self.reentry_cooldown_ticks = max(0, int(config.get("reentry_cooldown_ticks", 3)))
            self.premium_min_move = float(config.get("premium_min_move", 0.5))
            self.opposite_weakness_threshold = float(
                config.get("opposite_weakness_threshold", 0)
            )
            self.hard_stop_loss_points = float(
                config.get("hard_stop_loss_points", self.initialSL)
            )
            self.profit_protection_start = float(
                config.get("profit_protection_start", config.get("target_for_safe_sl", self.initialSL))
            )
            self.profit_lock_points = float(config.get("profit_lock_points", config.get("safe_sl", 0)))
            self.premium_trailing_stop_points = float(
                config.get("premium_trailing_stop_points", config.get("trailing_points", self.initialSL))
            )

            # A pair is frozen for a monitoring round.  This prevents an ATM
            # move from changing the instrument halfway through confirmation.
            self.monitoring_symbols = None
            self.should_continue = config.get("_should_continue", lambda: True)

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

    @staticmethod
    def _as_bool(value):
        """Accept booleans from both Django values and string-based config."""
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in {"1", "true", "yes", "on"}

    def _is_running(self):
        """Return the task's database-backed run state without exposing DB details here."""
        try:
            return bool(self.should_continue())
        except Exception as e:
            addLogDetails(ERROR, f"[premium-pair] Unable to check Flash run status: {e}")
            return False

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

    def _build_option_symbol(self, direction, atm_strike):
        """Build the same CE/PE contracts used by the existing Flash strategy."""
        strike_offset = self.strike if direction == "CE" else -self.strike
        return f"{getTradingSymbol(self.index_name)}{atm_strike + strike_offset}{direction}"

    def _get_monitoring_symbols(self):
        """Return a stable CE/PE pair for the current monitoring round."""
        if self.monitoring_symbols is None:
            atm_strike = self.BrokerObject.getCurrentAtm(self.index_name)
            self.monitoring_symbols = {
                "CE": self._build_option_symbol("CE", atm_strike),
                "PE": self._build_option_symbol("PE", atm_strike),
            }
            addLogDetails(
                INFO,
                f"[premium-pair] Monitoring CE={self.monitoring_symbols['CE']} "
                f"and PE={self.monitoring_symbols['PE']}",
            )
        return self.monitoring_symbols

    def _get_premium_price(self, symbol):
        details = self.BrokerObject.getCurrentPremiumDetails(NFO, symbol)
        price = float(self.BrokerObject.getLtpForPremium(details))
        if price <= 0:
            raise ValueError(f"Invalid premium price for {symbol}: {price}")
        return price

    def _fetch_premium_pair(self):
        """Fetch CE and PE concurrently, so both values represent one tick."""
        symbols = self._get_monitoring_symbols()
        with ThreadPoolExecutor(max_workers=2) as executor:
            ce_future = executor.submit(self._get_premium_price, symbols["CE"])
            pe_future = executor.submit(self._get_premium_price, symbols["PE"])
            prices = {"CE": ce_future.result(), "PE": pe_future.result()}
        return symbols, prices

    def _get_entry_signal(self, changes):
        """Return the side that is strong only when its paired option is weak."""
        ce_change = changes["CE"]
        pe_change = changes["PE"]
        minimum_gap = self.premium_min_move

        ce_is_stronger = (
            ce_change >= self.premium_min_move
            and pe_change <= self.opposite_weakness_threshold
            and ce_change - pe_change >= minimum_gap
        )
        pe_is_stronger = (
            pe_change >= self.premium_min_move
            and ce_change <= self.opposite_weakness_threshold
            and pe_change - ce_change >= minimum_gap
        )
        if ce_is_stronger:
            return "CE"
        if pe_is_stronger:
            return "PE"
        return None

    def _is_confirmed_reversal(self, active_side, changes):
        opposite_side = "PE" if active_side == "CE" else "CE"
        active_change = changes[active_side]
        opposite_change = changes[opposite_side]
        return (
            active_change <= -self.premium_min_move
            and opposite_change >= self.premium_min_move
            and opposite_change - active_change >= self.premium_min_move
        )

    @staticmethod
    def _next_streak(previous_signal, previous_streak, new_signal):
        if not new_signal:
            return None, 0
        if new_signal == previous_signal:
            return new_signal, previous_streak + 1
        return new_signal, 1

    @staticmethod
    def _price_or_fallback(value, fallback):
        try:
            price = float(value)
            return price if price > 0 else fallback
        except (TypeError, ValueError):
            return fallback

    def _enter_premium_trade(self, direction, symbol):
        if direction == "CE":
            return self.startCE(symbol)
        return self.startPE(symbol)

    def evaluatePriceAction(self):
        """
        Trade only a confirmed CE-vs-PE premium imbalance.

        Unlike the earlier index-only loop, every decision is made from the
        change in *both* premiums.  A normal pullback cannot close a position:
        exits require either a hard loss limit, a confirmed trailing breach, or
        a confirmed reversal where the opposite option is strengthening.
        """
        try:
            previous_prices = None
            entry_signal = None
            entry_streak = 0
            active_trade = None
            cooldown_ticks = 0

            while True:
                time.sleep(self.monitor_interval_seconds)

                # Keep the existing pivot status up to date, but do not make
                # option entries wait for an unrelated index-breakout signal.
                if not self.isPivotDecided:
                    self.checkAndSetPivot()
                try:
                    symbols, prices = self._fetch_premium_pair()
                except Exception as e:
                    addLogDetails(ERROR, f"[premium-pair] Unable to fetch CE/PE prices: {e}")
                    continue

                # UI Stop is cooperative: do not take a new entry, and close
                # an existing option at the current paired-premium price.
                # Retrying on a failed exit avoids silently leaving a live
                # position open while the task disappears.
                if not self._is_running():
                    if active_trade is not None:
                        side = active_trade["side"]
                        if not self.exitBasedOnCondition(
                            prices[side], "Flash stop requested from UI"
                        ):
                            continue
                    addLogDetails(INFO, "[premium-pair] Flash task stopped by user")
                    return

                if previous_prices is None:
                    previous_prices = prices
                    addLogDetails(INFO, f"[premium-pair] Baseline CE={prices['CE']:.2f}, PE={prices['PE']:.2f}")
                    continue

                changes = {
                    "CE": prices["CE"] - previous_prices["CE"],
                    "PE": prices["PE"] - previous_prices["PE"],
                }
                previous_prices = prices
                addLogDetails(
                    INFO,
                    f"[premium-pair] CE={prices['CE']:.2f} ({changes['CE']:+.2f}) | "
                    f"PE={prices['PE']:.2f} ({changes['PE']:+.2f})",
                )

                if active_trade is None:
                    if cooldown_ticks:
                        cooldown_ticks -= 1
                        entry_signal, entry_streak = None, 0
                        continue

                    candidate = self._get_entry_signal(changes)
                    entry_signal, entry_streak = self._next_streak(
                        entry_signal, entry_streak, candidate
                    )
                    if entry_signal and entry_streak >= self.entry_confirmation_ticks:
                        if self._enter_premium_trade(entry_signal, symbols[entry_signal]):
                            actual_entry = self._price_or_fallback(
                                self.optionBuyPrice, prices[entry_signal]
                            )
                            active_trade = {
                                "side": entry_signal,
                                "entry_price": actual_entry,
                                "highest_price": actual_entry,
                                "hold_ticks": 0,
                                "reversal_streak": 0,
                                "trailing_breach_streak": 0,
                            }
                            entry_signal, entry_streak = None, 0
                            addLogDetails(
                                INFO,
                                f"[premium-pair] Entered {active_trade['side']} at {actual_entry:.2f} "
                                f"after {self.entry_confirmation_ticks} confirming ticks",
                            )
                        else:
                            # A rejected order must receive fresh confirmation.
                            entry_signal, entry_streak = None, 0
                    continue

                side = active_trade["side"]
                option_price = prices[side]
                active_trade["hold_ticks"] += 1
                active_trade["highest_price"] = max(active_trade["highest_price"], option_price)

                # This is intentionally immediate.  It is the only exit that
                # can override confirmation because it bounds maximum loss.
                if option_price <= active_trade["entry_price"] - self.hard_stop_loss_points:
                    reason = (
                        f"Hard safety stop: {option_price:.2f} <= "
                        f"{active_trade['entry_price'] - self.hard_stop_loss_points:.2f}"
                    )
                    if self.exitBasedOnCondition(option_price, reason):
                        active_trade = None
                        cooldown_ticks = self.reentry_cooldown_ticks
                        self.monitoring_symbols = None
                        previous_prices = None
                    continue

                if active_trade["highest_price"] >= (
                    active_trade["entry_price"] + self.profit_protection_start
                ):
                    protected_stop = max(
                        active_trade["entry_price"] + self.profit_lock_points,
                        active_trade["highest_price"] - self.premium_trailing_stop_points,
                    )
                    if option_price <= protected_stop:
                        active_trade["trailing_breach_streak"] += 1
                    else:
                        active_trade["trailing_breach_streak"] = 0

                    if (
                        active_trade["trailing_breach_streak"]
                        >= self.trailing_exit_confirmation_ticks
                    ):
                        reason = (
                            f"Confirmed profit-protection exit: {option_price:.2f} <= "
                            f"{protected_stop:.2f} for {self.trailing_exit_confirmation_ticks} ticks"
                        )
                        if self.exitBasedOnCondition(option_price, reason):
                            active_trade = None
                            cooldown_ticks = self.reentry_cooldown_ticks
                            self.monitoring_symbols = None
                            previous_prices = None
                        continue

                if self._is_confirmed_reversal(side, changes):
                    active_trade["reversal_streak"] += 1
                else:
                    active_trade["reversal_streak"] = 0

                if (
                    active_trade["hold_ticks"] >= self.minimum_hold_ticks
                    and active_trade["reversal_streak"] >= self.exit_confirmation_ticks
                ):
                    reason = (
                        f"Confirmed CE/PE reversal after {active_trade['reversal_streak']} ticks"
                    )
                    if self.exitBasedOnCondition(option_price, reason):
                        active_trade = None
                        cooldown_ticks = self.reentry_cooldown_ticks
                        self.monitoring_symbols = None
                        previous_prices = None
        except Exception as e:
            addLogDetails(ERROR, f"[evaluatePriceAction] Error: {e}")

    def startCE(self, option_symbol=None):
        try:
            if not self.isCEOrderPlaced:
                print("CE not placed")
                self.resetPEFlag()
                self.CESetTargetAndStopLoss()
                return self.placeOrder("CE", self.strike, option_symbol)
            else:
                print("CE already placed")
                return False
        except Exception as e:
            addLogDetails(ERROR, f"[startCE] Error: {e}")
            return False

    def startPE(self, option_symbol=None):
        try:
            if not self.isPEOrderPlaced:
                self.resetCEFlag()
                self.PESetTargetAndStoploss()
                return self.placeOrder("PE", -self.strike, option_symbol)
            else:
                print("PE is already placed")
                return False
        except Exception as e:
            addLogDetails(ERROR, f"[startPE] Error: {e}")
            return False

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

    def placeOrder(self, direction: str, strike_offset: int, option_symbol=None):
        try:
            if option_symbol:
                optionToBuy = option_symbol
            else:
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
                return True
            addLogDetails(ERROR, f"[placeOrder] {direction} order was rejected: {order_response}")
            return False
        except Exception as e:
            addLogDetails(ERROR, f"User: {self.user_email} exception in place{direction} ---- {e}")
            return False

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
                try:
                    sl_price = float(self.optionBuyPrice) - self.initialSL
                    sl_order_details = self._prepareOrderDetails(
                        option_symbol, SELL, ORDER_TYPE_SL, price=sl_price, trigger_price=sl_price
                    )
                    sl_order = self.BrokerObject.placeOrder(sl_order_details)
                    if sl_order.get("message") == "SUCCESS":
                        self.currentExitOrderID = sl_order["data"]["orderid"]
                        self.isStoplossPlaced = True
                    else:
                        addLogDetails(ERROR, f"[placeOrder] Protective SL rejected: {sl_order}")
                except Exception as e:
                    addLogDetails(ERROR, f"[placeOrder] Protective SL was not placed: {e}")

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
                if self.is_place_sl_required and self.isStoplossPlaced and self.currentExitOrderID:
                    # The pending order is the stop-loss SELL order, not the
                    # completed BUY order.  Modify that order to market to
                    # close safely without creating a second SELL order.
                    if self.BrokerObject.checkIfOrderExists(self.currentExitOrderID):
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
                        if not modify_order_response:
                            addLogDetails(ERROR, "[exitBasedOnCondition] Stop-loss exit modification failed")
                            return False
                        addLogDetails(INFO,
                                      f"Index Name: {self.index_name} | User: {self.user_email} | ExitOrder: {modify_order_response}")
                        addLogDetails(INFO, "Order exited successfully")

                    else:
                        addLogDetails(INFO,
                                      f"Index Name: {self.index_name} | User: {self.user_email} | "
                                      "Stop-loss order is no longer pending; it may already be filled")
                else:
                    order_details = self._prepareOrderDetails(self.currentPremiumPlaced, SELL, MARKET)
                    addLogDetails(INFO,
                                  f"Index Name: {self.index_name} User: {self.user_email} {order_details}")

                    order_response = self.BrokerObject.placeOrder(order_details)
                    if order_response.get("message") != "SUCCESS":
                        addLogDetails(ERROR, f"[exitBasedOnCondition] Exit order rejected: {order_response}")
                        return False

            # The paired premium from the monitoring tick is the best price
            # available at the decision point.  Do not mistakenly write the
            # entry order's average price as the exit price.
            self.optionExitPrice = fromOptionPrice
            data = {
                USER_ID: self.user_email,
                SCRIPT_NAME: self.currentPremiumPlaced,
                QTY: self.user_qty,
                EXIT_PRICE: self.optionExitPrice,
                STATUS: ORDER_EXITED
            }
            addOrderBookDetails(data, False)

            # A completed exit must permit a fresh, independently confirmed
            # trade; retaining either flag blocked all later entries.
            self.currentOrderID = None
            self.currentExitOrderID = None
            self.optionExitPrice = None
            self.isStoplossPlaced = False
            self.isCEOrderPlaced = False
            self.isPEOrderPlaced = False
            self.optionDetails = None
            self.optionBuyPrice = None
            self.currentPremiumPlaced = None
            self.exitConditions = []

            addLogDetails(INFO,
                          f"Index Name: {self.index_name} | User: {self.user_email} | Exit conditions: {self.exitConditions}")
            return True

        except Exception as e:
            addLogDetails(ERROR, f"{self.index_name} | Exception in exitBasedOnCondition: {e}")
            return False

    def revertDummyOrder(self, fromOptionPrice):
        addLogDetails(INFO, "Index Name: " + self.index_name + " User :" + self.user_email + " revertDummyOrder")
        order_response = {'message': 'SUCCESS', 'data': {'order_id': 'exit_dummy_id'}}
        self.optionExitPrice = fromOptionPrice
        data = {USER_ID: self.user_email, SCRIPT_NAME: self.currentPremiumPlaced, QTY: self.user_qty,
                EXIT_PRICE: self.optionExitPrice, STATUS: ORDER_EXITED}
        addLogDetails(INFO, "Index Name: " + self.index_name + " User :" + self.user_email + " " + str(data))
        return order_response
