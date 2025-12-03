from plutusAI.models import ManualOrders
from plutusAI.server.base import addLogDetails, getTradingSymbol, addOrderBookDetails
from plutusAI.server.constants import *

from SmartApi.smartWebSocketV2 import SmartWebSocketV2
import time
import traceback

class HighFrequencyTrading:
    def __init__(self, index_name, user_email, BrokerObject, target_points: int = 50):
        """
        target_points: points target (e.g., 50). Global money target = target_points * user_qty
        """
        self.index_name = index_name
        self.user_email = user_email
        self.BrokerObject = BrokerObject
        self.is_demo_enabled = self.BrokerObject.is_demo_enabled

        # default qty (may be overwritten from DB-derived settings below)
        self.user_qty = 75

        # per-token small windows and persistent trade states
        self.trade_states = {}
        self.correlation_id = "admin_ws"

        # global pnl and profit lock
        self.global_pnl = 0.0
        self.target_points = target_points
        self.max_target_profit_money = None  # will set after user_qty determined
        self.trading_active = True
        self.sws = None
        self._shutdown_in_progress = False

        # prepare symbols from your broker / DB like original code
        atm_strike = self.BrokerObject.getCurrentAtm(self.index_name)
        strike_offset = 100  # your chosen offset
        CE_option = f"{getTradingSymbol(self.index_name)}{atm_strike - strike_offset}{'CE'}"
        PE_option = f"{getTradingSymbol(self.index_name)}{atm_strike + strike_offset}{'PE'}"

        # read user/manual config from DB (same as you had)
        user_manual_details = ManualOrders.objects.filter(user_id=user_email, index_name=self.index_name)
        user_index_data = list(user_manual_details.values())[0]
        self.product_type = user_index_data.get(PRODUCT_TYPE)

        # derive per-order quantity using your existing logic
        index_qty = int(75)
        qty_multiplier = int(5)
        self.user_qty = qty_multiplier * index_qty

        # set money target based on points * qty (Option 2)
        self.max_target_profit_money = float(self.target_points * self.user_qty)

        # prepare trading symbols / tokens exactly like original
        self.trading_symbols = [CE_option, PE_option]
        print("Trading symbols:", self.trading_symbols)
        self.tokens_list = [BrokerObject.getTokenForSymbol(sym) for sym in self.trading_symbols]
        self.symbol_token_map = [{"symbol": self.trading_symbols[i], "token": self.tokens_list[i]} for i in range(len(self.trading_symbols))]
        self.all_token_list = [{"exchangeType": 2, "tokens": self.tokens_list}]
        print("Subscription list:", self.all_token_list)

        # init per-token trade state
        for token in self.tokens_list:
            self.trade_states[token] = {
                "price_window": [],        # lastFiveBuyOrder (int price as you were storing)
                "buy_qty_window": [],      # last_no_buy_order
                "sell_qty_window": [],     # last_no_sell_order
                "base_price": None,        # candidate base (oldest in window)
                "sl": None,                # active SL reference
                "in_position": False,      # bool
                "entry_price": None,       # weighted avg entry price (float)
                "position_qty": 0,         # total qty currently held (int)
                "avg_count": 0,            # how many averages done (max 2)
                "printed_waiting": False   # helper to avoid repeated log messages
            }

        # store DB-derived status; we'll only connect WS if DB status == "running"
        self.db_status = user_index_data.get("status", "running")
        print(f"DB status: {self.db_status}  (WebSocket will start only if 'running')")

    def get_symbol_from_token(self, token_to_find):
        for item in self.symbol_token_map:
            if item["token"] == token_to_find:
                return item["symbol"]
        return None

    # helper to place a buy (demo vs live)
    def _place_buy(self, token, ltp, qty):
        symbol = self.get_symbol_from_token(token)
        if self.is_demo_enabled:
            order_data = {
                USER_ID: self.user_email,
                SCRIPT_NAME: symbol,
                QTY: qty,
                ENTRY_PRICE: ltp,
                STATUS: ORDER_PLACED,
                STRATEGY: STRATEGY_HUNTER,
                INDEX_NAME: self.index_name
            }
            addOrderBookDetails(order_data, True)
            return {"demo": True, "detail": order_data}
        else:
            order_details = {
                VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: symbol,
                SYMBOL_TOKEN: token,
                TRANSACTION_TYPE: BUY,
                ORDER_TYPE: MARKET, PRODUCT_TYPE: self.product_type,
                DURATION: DAY, QUANTITY: qty
            }
            return self.BrokerObject.placeOrder(order_details)

    # helper to place a single SELL of full qty (Option A)
    def _place_sell_total(self, token, qty, ltp=None):
        symbol = self.get_symbol_from_token(token)
        if self.is_demo_enabled:
            data = {
                USER_ID: self.user_email,
                SCRIPT_NAME: symbol,
                QTY: qty,
                EXIT_PRICE: ltp,
                STATUS: ORDER_EXITED
            }
            addOrderBookDetails(data, False)
            return {"demo": True, "detail": data}
        else:
            order_details = {
                VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: symbol,
                SYMBOL_TOKEN: token,
                TRANSACTION_TYPE: SELL,
                ORDER_TYPE: MARKET, PRODUCT_TYPE: self.product_type,
                DURATION: DAY, QUANTITY: qty
            }
            return self.BrokerObject.placeOrder(order_details)

    # compute realized pnl for an exit and update global tally
    def _record_realized_pnl_and_check(self, token, exit_price, qty, entry_price):
        """
        Realized PnL calculation:
          pnl = (exit_price - entry_price) * qty
        (for options you are buying; profit when exit_price > entry_price)
        """
        # if exit_price is None or 0, use entry_price as safe fallback (pnl 0)
        if exit_price is None:
            pnl = 0.0
        else:
            pnl = (exit_price - entry_price) * qty
        self.global_pnl += pnl
        addLogDetails(INFO, f"[PnL] Token {token} realized pnl {pnl:.2f}. Global pnl={self.global_pnl:.2f} / target={self.max_target_profit_money:.2f}")
        return self.global_pnl >= self.max_target_profit_money

    # graceful global shutdown: exit everything, close ws, update status
    def _global_shutdown(self):
        if self._shutdown_in_progress:
            return
        self._shutdown_in_progress = True
        addLogDetails(INFO, f"[GlobalShutdown] Target reached. Exiting all positions and stopping trading. Global PnL={self.global_pnl:.2f}")

        # exit each token if in position
        for token, state in self.trade_states.items():
            if state.get("in_position") and state.get("position_qty", 0) > 0:
                qty_to_exit = state["position_qty"]
                try:
                    resp = self._place_sell_total(token, qty_to_exit, None)
                    addLogDetails(INFO, f"[GlobalShutdown] Exit placed for token {token} qty={qty_to_exit} resp={resp}")
                    # compute realized pnl using entry price and the best available fallback (we don't have fill price here)
                    entry_price = state.get("entry_price") or 0.0
                    # We don't have synchronous fill price so pass entry_price as fallback -> pnl 0 in worst case.
                    self._record_realized_pnl_and_check(token, None, qty_to_exit, entry_price)
                except Exception as e:
                    addLogDetails(ERROR, f"[GlobalShutdown] Error placing exit for token {token}: {e}")

                # reset token state
                state["in_position"] = False
                state["entry_price"] = None
                state["position_qty"] = 0
                state["avg_count"] = 0
                state["price_window"] = []
                state["buy_qty_window"] = []
                state["sell_qty_window"] = []
                state["base_price"] = None
                state["sl"] = None
                state["printed_waiting"] = False

        # disconnect websocket safely
        try:
            if self.sws:
                try:
                    self.sws.disconnect()
                    addLogDetails(INFO, "[GlobalShutdown] WebSocket disconnected.")
                except Exception as e:
                    addLogDetails(ERROR, f"[GlobalShutdown] Error disconnecting websocket: {e}")
        finally:
            # mark trading inactive and (optionally) update DB status
            self.trading_active = False
            try:
                ManualOrders.objects.filter(user_id=self.user_email, index_name=self.index_name).update(status='stopped')
            except Exception as e:
                addLogDetails(ERROR, f"[GlobalShutdown] Error updating DB status: {e}")
            addLogDetails(INFO, "[GlobalShutdown] Trading stopped for the day (MAX_PROFIT_REACHED).")

    # === This is the entry point similar to your original startHFT() ===
    def startHFT(self):
        def on_open(wsapp):
            addLogDetails(INFO, f"[WebSocket] Connection opened. Subscribing to tokens: {self.all_token_list}")
            try:
                sws.subscribe(self.correlation_id, 3, self.all_token_list)
            except Exception as e:
                addLogDetails(ERROR, f"[on_open] Subscribe failed: {e}")

        def on_data(wsapp, message):
            # Fast guard: if global kill switch triggered, ignore ticks
            if not self.trading_active:
                return

            try:
                # message is already a dict (as you had), do not parse
                data = message

                token = data.get("token")
                ltp_raw = data.get("last_traded_price")
                best_5_buy = data.get("best_5_buy_data", [])
                best_5_sell = data.get("best_5_sell_data", [])

                # basic validation
                if token is None or ltp_raw is None or not best_5_buy or not best_5_sell:
                    return

                ltp = ltp_raw / 100.0

                best_buy_price = best_5_buy[0].get("price")
                best_buy_qty = int(best_5_buy[0].get("quantity", 0))
                best_sell_qty = int(best_5_sell[0].get("quantity", 0))

                if best_buy_price is None:
                    return

                best_buy_price_f = best_buy_price / 100.0
                # store as integer like original code did
                best_buy_price_int = int(best_buy_price_f)

                # ensure token state exists
                if token not in self.trade_states:
                    # safety init (shouldn't happen normally)
                    self.trade_states[token] = {
                        "price_window": [],
                        "buy_qty_window": [],
                        "sell_qty_window": [],
                        "base_price": None,
                        "sl": None,
                        "in_position": False,
                        "entry_price": None,
                        "position_qty": 0,
                        "avg_count": 0,
                        "printed_waiting": False
                    }
                    print(self.trade_states)
                state = self.trade_states[token]

                # update rolling windows
                if best_buy_price_int not in state["price_window"]:
                    state["price_window"].append(best_buy_price_int)
                state["buy_qty_window"].append(best_buy_qty)
                state["sell_qty_window"].append(best_sell_qty)

                if len(state["price_window"]) > 5:
                    state["price_window"].pop(0)
                if len(state["buy_qty_window"]) > 5:
                    state["buy_qty_window"].pop(0)
                if len(state["sell_qty_window"]) > 5:
                    state["sell_qty_window"].pop(0)

                # wait until we have 5 samples
                if len(state["price_window"]) < 5:
                    if not state["printed_waiting"]:
                        state["printed_waiting"] = True
                    return

                # compute averages
                avg_price = sum(state["price_window"]) / len(state["price_window"])
                avg_buy_qty = sum(state["buy_qty_window"]) / len(state["buy_qty_window"])
                avg_sell_qty = sum(state["sell_qty_window"]) / len(state["sell_qty_window"])

                # base price init or trailing update: candidate = oldest in window
                candidate_base = state["price_window"][0]
                if state["base_price"] is None:
                    state["base_price"] = candidate_base
                    state["sl"] = candidate_base
                else:
                    # only update SL when candidate_base > current sl (trailing upward)
                    if candidate_base > state["sl"] and not state["in_position"]:
                        state["base_price"] = candidate_base
                        state["sl"] = candidate_base

                base = state["base_price"]
                sl = state["sl"]

                # ENTRY logic: only if not in position
                if not state["in_position"]:
                    if avg_price > base and avg_buy_qty > avg_sell_qty and self.trading_active:
                        # place BUY
                        print(f"✅ [BUY ENTRY] Token {token} | Avg={avg_price:.2f} > Base={base:.2f} | LTP={ltp} | Symbol={self.get_symbol_from_token(token)}")
                        resp = self._place_buy(token, ltp, self.user_qty)
                        print("BUY response:", resp)

                        # set position state
                        state["in_position"] = True
                        state["entry_price"] = ltp
                        state["position_qty"] = self.user_qty
                        state["avg_count"] = 0
                        # clear windows after entry to avoid immediate re-trigger
                        state["price_window"] = []
                        state["buy_qty_window"] = []
                        state["sell_qty_window"] = []
                        state["printed_waiting"] = False
                        print("State :", state)

                if (
                        state["in_position"] and state["avg_count"] < 2 and
                        ltp < (state["entry_price"] - 2)
                ):
                    print(
                        f"➕ [AVERAGE] Token {token} | LTP={ltp} below midpoint -> averaging. Prev entry={state['entry_price']}, SL={sl}")
                    resp = self._place_buy(token, ltp, self.user_qty)
                    print("AVERAGE BUY response:", resp)

                    # weighted average entry price update
                    old_entry = state["entry_price"]
                    old_qty = state["position_qty"]
                    add_qty = self.user_qty
                    new_total_qty = old_qty + add_qty
                    new_entry_price = ((old_entry * old_qty) + (ltp * add_qty)) / new_total_qty

                    state["entry_price"] = new_entry_price
                    state["position_qty"] = new_total_qty
                    state["avg_count"] += 1

                    # per your rule, SL remains unchanged
                    # clear windows to avoid immediate retrigger
                    state["price_window"] = []
                    state["buy_qty_window"] = []
                    state["sell_qty_window"] = []
                    state["printed_waiting"] = False
                    print("State :", state)


                else:
                    # IN POSITION: check EXIT or AVERAGE
                    # FIRST: EXIT conditions  ##  or avg_buy_qty < avg_sell_qty
                    if ltp <= sl or avg_buy_qty < avg_sell_qty:
                        total_qty_to_exit = state["position_qty"]
                        if total_qty_to_exit > 0:
                            print(f"🛑 [EXIT] Token {token} | LTP={ltp} <= SL={sl} or imbalance detected. Exiting {total_qty_to_exit}")
                            resp = self._place_sell_total(token, total_qty_to_exit, ltp)
                            print("EXIT response:", resp)
                            # compute realized pnl and update global_pnl
                            entry_price = state.get("entry_price") or 0.0
                            reached = self._record_realized_pnl_and_check(token, ltp, total_qty_to_exit, entry_price)

                            # reset token state
                            state["in_position"] = False
                            state["entry_price"] = None
                            state["position_qty"] = 0
                            state["avg_count"] = 0
                            state["price_window"] = []
                            state["buy_qty_window"] = []
                            state["sell_qty_window"] = []
                            state["printed_waiting"] = False
                            state["base_price"] = None
                            state["sl"] = None
                            print("State :",self.global_pnl)


                            # if we've reached the global target, shutdown everything
                            if reached:
                                self._global_shutdown()
                                return

                    #else:
                        # AVERAGING check (only if avg_count < 2)
                        # condition: ltp < entry_price - ((entry_price - sl) / 2) and ltp > sl and avg_buy_qty > avg_sell_qty


            except Exception as e:
                # robust logging
                try:
                    token_info = message.get("token")
                except Exception:
                    token_info = "unknown"
                addLogDetails(ERROR, f"[on_data] Error for token {token_info}: {e}")
                print("Exception in on_data:", e)
                traceback.print_exc()

        def on_error(wsapp, error):
            addLogDetails(ERROR, f"[WebSocket] Error: {error}")

        def on_close(wsapp):
            addLogDetails(INFO, "[WebSocket] Connection closed.")

        def create_websocket():
            # create SmartWebSocketV2 exactly like your original working code
            ws = SmartWebSocketV2(
                self.BrokerObject.auth_token,
                self.BrokerObject.broker_api_token,
                self.BrokerObject.broker_user_id,
                self.BrokerObject.feed_token,
                max_retry_attempt=2
            )
            # assign callbacks (these names must match SmartWebSocketV2 expected attributes)
            ws.on_open = on_open
            ws.on_data = on_data
            ws.on_error = on_error
            ws.on_close = on_close
            return ws

        # only try to connect if DB status says running
        if str(self.db_status).lower() != "running":
            addLogDetails(INFO, f"[startHFT] DB status is '{self.db_status}' -> not starting websocket.")
            print(f"[startHFT] DB status is '{self.db_status}' -> WS NOT started.")
            return

        MAX_RETRIES = 3
        RETRY_DELAY = 5

        # create sws and connect (retain your original retry behaviour)
        for attempt in range(MAX_RETRIES):
            try:
                sws = create_websocket()
                # store reference for shutdown
                self.sws = sws
                sws.connect()
                break
            except Exception as e:
                addLogDetails(ERROR, f"[Retry {attempt + 1}] WebSocket connection failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    addLogDetails(ERROR, "WebSocket failed after maximum retries.")
