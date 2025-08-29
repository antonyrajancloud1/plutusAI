from plutusAI.server.base import addLogDetails, getTradingSymbol, addOrderBookDetails
from plutusAI.server.constants import *

from SmartApi.smartWebSocketV2 import SmartWebSocketV2
import time

class HighFrequencyTrading:
    def __init__(self, index_name, user_email, BrokerObject):
        self.index_name = index_name
        self.user_email = user_email
        self.BrokerObject = BrokerObject
        self.is_demo_enabled = self.BrokerObject.is_demo_enabled
        self.user_qty=75
        self.tick_data = {}
        self.correlation_id = "admin_ws"
        atm_strike = self.BrokerObject.getCurrentAtm(self.index_name)
        strike_offset=100 #ATM -100
        CE_option = f"{getTradingSymbol(self.index_name)}{atm_strike - strike_offset}{'CE'}"
        PE_option = f"{getTradingSymbol(self.index_name)}{atm_strike + strike_offset}{'PE'}"

        self.trading_symbols = [CE_option, PE_option]
        self.tokens_list = [BrokerObject.getTokenForSymbol(sym) for sym in self.trading_symbols]
        self.symbol_token_map = [{"symbol": self.trading_symbols[0], "token": self.tokens_list[0]},
                            {"symbol": self.trading_symbols[1], "token": self.tokens_list[1]}]
        self.all_token_list = [{"exchangeType": 2, "tokens": self.tokens_list}]
        print(self.all_token_list)
            # 🟡 Per-token tracking
        trade_states = {
            token: {
                "price_data": [],
                "position": None,
                "entry_price": None,
                "net_total_pnl": 0,
                "buyCompleted": False
            }
            for token in self.tokens_list
        }
    def get_symbol_from_token(self,token_to_find):
        for item in self.symbol_token_map:
            if item["token"] == token_to_find:
                return item["symbol"]
        return None
    def startHFT(self):
        def on_open(wsapp):
            addLogDetails(INFO, f"[WebSocket] Connection opened. Subscribing to tokens: {self.all_token_list}")
            sws.subscribe(self.correlation_id, 3, self.all_token_list)

        def on_data(wsapp, message):

            try:
                # print(tick_data)
                # ✅ message is already a dict, do not parse again
                data = message
                token = data.get("token")
                ltp = data.get("last_traded_price")/100
                ltp_whole = int(ltp)
                best_5_buy = data.get("best_5_buy_data", [])

                if token is None or ltp is None or not best_5_buy:
                    return

                best_buy_price = int(best_5_buy[0]["price"]/100)
                # print(best_buy_price)

                if token not in self.tick_data:
                    self.tick_data[token] = {
                        "base_price": ltp,
                        "lastFiveBuyOrder": [],
                        "in_position": False,
                        "sl": None,
                        "printed_waiting": False
                    }
                    print(f"📌 Token {token}: Base price set to {ltp}")

                token_data = self.tick_data[token]
                if best_buy_price not in token_data["lastFiveBuyOrder"]:
                    token_data["lastFiveBuyOrder"].append(best_buy_price)
                if len(token_data["lastFiveBuyOrder"]) > 5:
                    token_data["lastFiveBuyOrder"].pop(0)

                if len(token_data["lastFiveBuyOrder"]) < 5:
                    if not token_data["printed_waiting"]:
                        # print(f"⏳ Token {token}: Waiting for 5 prices... ({len(token_data['lastFiveBuyOrder'])}/5)")
                        token_data["printed_waiting"] = True
                    return

                avg = sum(token_data["lastFiveBuyOrder"]) / 5
                # base = token_data["base_price"]
                base = token_data["lastFiveBuyOrder"][0]
                if not token_data["in_position"]:
                    # print(f"📈 Token {token}: Avg={avg:.2f}, Base={base:.2f} -> Waiting for avg > base")
                    if avg > base:
                        print(self.tick_data)
                        print(f"✅ [BUY] Token {token} | Avg={avg:.2f} > Base={base:.2f} | OptionBuyPrice={ltp}")
                        if self.is_demo_enabled:
                            order_data = {
                                USER_ID: self.user_email,
                                SCRIPT_NAME: self.get_symbol_from_token(token),
                                QTY: self.user_qty,
                                ENTRY_PRICE: ltp,
                                STATUS: ORDER_PLACED,
                                STRATEGY: STRATEGY_HUNTER,
                                INDEX_NAME: self.index_name
                            }
                            addOrderBookDetails(order_data, True)
                        token_data["in_position"] = True
                        token_data["sl"] = base
                        token_data["lastFiveBuyOrder"] = []
                        token_data["printed_waiting"] = False
                else:
                    # print(f"🔍 Token {token}: In position | Monitoring SL={token_data['sl']} | LTP={ltp}")
                    print(token + "  :  "+str(token_data["lastFiveBuyOrder"]))
                    if ltp <= token_data["lastFiveBuyOrder"][0]:
                        print(f"🛑 [EXIT] Token {token} | LTP={ltp} <= SL={token_data['sl']} | OptionBuyPrice={ltp}")
                        data = {
                            USER_ID: self.user_email,
                            SCRIPT_NAME:  self.get_symbol_from_token(token),
                            QTY: self.user_qty,
                            EXIT_PRICE: ltp,
                            STATUS: ORDER_EXITED
                        }
                        addOrderBookDetails(data, False)
                        token_data["in_position"] = False
                        token_data["lastFiveBuyOrder"] = []
                        token_data["printed_waiting"] = False

            except Exception as e:
                print(f"❌ Error in on_message: {e}")
                addLogDetails(ERROR, f"[on_data] Error for token {message.get('token')}: {e}")

        def on_error(wsapp, error):
            addLogDetails(ERROR, f"[WebSocket] Error: {error}")

        def on_close(wsapp):
            addLogDetails(INFO, "[WebSocket] Connection closed.")

        def create_websocket():
            ws = SmartWebSocketV2(
                self.BrokerObject.auth_token,
                self.BrokerObject.broker_api_token,
                self.BrokerObject.broker_user_id,
                self.BrokerObject.feed_token,
                max_retry_attempt=2
            )
            ws.on_open = on_open
            ws.on_data = on_data
            ws.on_error = on_error
            ws.on_close = on_close
            return ws

        MAX_RETRIES = 3
        RETRY_DELAY = 5

        for attempt in range(MAX_RETRIES):
            try:
                sws = create_websocket()
                sws.connect()
                break
            except Exception as e:
                addLogDetails(ERROR, f"[Retry {attempt + 1}] WebSocket connection failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    addLogDetails(ERROR, "WebSocket failed after maximum retries.")



