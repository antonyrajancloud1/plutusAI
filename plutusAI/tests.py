from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .server.broker.AngelOneBroker import AngelOneBroker
from .server.manualOrder import *
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
import time

from .server.priceAction.hft import HighFrequencyTrading


@require_http_methods(["GET"])
def tester(request):
    # try:
    #     tick_data = {}
    #     user_broker_data = BrokerDetails.objects.filter(
    #         user_id=ADMIN_USER_ID, index_group=INDIAN_INDEX
    #     )
    #     BrokerObject = AngelOneBroker(user_broker_data)
    #
    #     correlation_id = "admin_ws"
    #     trading_symbols = ["NIFTY31JUL2524650CE","NIFTY31JUL2524800PE"]
    #     tokens_for_candle = [BrokerObject.getTokenForSymbol(sym) for sym in trading_symbols]
    #     symbol_token_map =[{"symbol":trading_symbols[0],"token":tokens_for_candle[0]},{"symbol":trading_symbols[1],"token":tokens_for_candle[1]}]
    #     all_token_list = [{"exchangeType": 2, "tokens": tokens_for_candle}]
    #     print(all_token_list)
    #
    #     # 🟡 Per-token tracking
    #     trade_states = {
    #         token: {
    #             "price_data": [],
    #             "position": None,
    #             "entry_price": None,
    #             "net_total_pnl": 0,
    #             "buyCompleted": False
    #         }
    #         for token in tokens_for_candle
    #     }
    #
    #     def on_open(wsapp):
    #         addLogDetails(INFO, f"[WebSocket] Connection opened. Subscribing to tokens: {all_token_list}")
    #         sws.subscribe(correlation_id, 3, all_token_list)
    #
    #     def on_data(wsapp, message):
    #
    #         try:
    #             # print(tick_data)
    #             # ✅ message is already a dict, do not parse again
    #             data = message
    #             token = data.get("token")
    #             ltp = data.get("last_traded_price")/100
    #             ltp_whole = int(ltp)
    #             best_5_buy = data.get("best_5_buy_data", [])
    #
    #             if token is None or ltp is None or not best_5_buy:
    #                 return
    #
    #             best_buy_price = int(best_5_buy[0]["price"]/100)
    #             # print(best_buy_price)
    #
    #             if token not in tick_data:
    #                 tick_data[token] = {
    #                     "base_price": ltp,
    #                     "lastFiveBuyOrder": [],
    #                     "in_position": False,
    #                     "sl": None,
    #                     "printed_waiting": False
    #                 }
    #                 print(f"📌 Token {token}: Base price set to {ltp}")
    #
    #             token_data = tick_data[token]
    #             if best_buy_price not in token_data["lastFiveBuyOrder"]:
    #                 token_data["lastFiveBuyOrder"].append(best_buy_price)
    #             if len(token_data["lastFiveBuyOrder"]) > 5:
    #                 token_data["lastFiveBuyOrder"].pop(0)
    #
    #             if len(token_data["lastFiveBuyOrder"]) < 5:
    #                 if not token_data["printed_waiting"]:
    #                     # print(f"⏳ Token {token}: Waiting for 5 prices... ({len(token_data['lastFiveBuyOrder'])}/5)")
    #                     token_data["printed_waiting"] = True
    #                 return
    #
    #             avg = sum(token_data["lastFiveBuyOrder"]) / 5
    #             # base = token_data["base_price"]
    #             base = token_data["lastFiveBuyOrder"][0]
    #             if not token_data["in_position"]:
    #                 # print(f"📈 Token {token}: Avg={avg:.2f}, Base={base:.2f} -> Waiting for avg > base")
    #                 if avg > base:
    #                     print(tick_data)
    #                     print(f"✅ [BUY] Token {token} | Avg={avg:.2f} > Base={base:.2f} | OptionBuyPrice={ltp}")
    #                     token_data["in_position"] = True
    #                     token_data["sl"] = base
    #                     token_data["lastFiveBuyOrder"] = []
    #                     token_data["printed_waiting"] = False
    #             else:
    #                 # print(f"🔍 Token {token}: In position | Monitoring SL={token_data['sl']} | LTP={ltp}")
    #                 print(token + "  :  "+str(token_data["lastFiveBuyOrder"]))
    #                 if ltp <= token_data["lastFiveBuyOrder"][0]:
    #                     print(f"🛑 [EXIT] Token {token} | LTP={ltp} <= SL={token_data['sl']} | OptionBuyPrice={ltp}")
    #                     token_data["in_position"] = False
    #                     token_data["lastFiveBuyOrder"] = []
    #                     token_data["printed_waiting"] = False
    #
    #         except Exception as e:
    #             print(f"❌ Error in on_message: {e}")
    #             addLogDetails(ERROR, f"[on_data] Error for token {message.get('token')}: {e}")
    #
    #
    #
    #
    #     def on_error(wsapp, error):
    #         addLogDetails(ERROR, f"[WebSocket] Error: {error}")
    #
    #     def on_close(wsapp):
    #         addLogDetails(INFO, "[WebSocket] Connection closed.")
    #
    #     def create_websocket():
    #         ws = SmartWebSocketV2(
    #             BrokerObject.auth_token,
    #             BrokerObject.broker_api_token,
    #             BrokerObject.broker_user_id,
    #             BrokerObject.feed_token,
    #             max_retry_attempt=2
    #         )
    #         ws.on_open = on_open
    #         ws.on_data = on_data
    #         ws.on_error = on_error
    #         ws.on_close = on_close
    #         return ws
    #
    #     MAX_RETRIES = 3
    #     RETRY_DELAY = 5
    #
    #     for attempt in range(MAX_RETRIES):
    #         try:
    #             sws = create_websocket()
    #             sws.connect()
    #             break
    #         except Exception as e:
    #             addLogDetails(ERROR, f"[Retry {attempt + 1}] WebSocket connection failed: {e}")
    #             if attempt < MAX_RETRIES - 1:
    #                 time.sleep(RETRY_DELAY)
    #             else:
    #                 addLogDetails(ERROR, "WebSocket failed after maximum retries.")
    #
    # except Exception as main_e:
    #     addLogDetails(ERROR, f"[Main Task Error] {main_e}")
    user_email = "antonyrajan.d@gmail.com"

    index_data = IndexDetails.objects.filter(index_name="nifty")
    index_group_name = get_index_group_name(index_data)
    if index_group_name == INDIAN_INDEX:
        # FlashTrade(user_email, index, INDIAN_INDEX)
        broker_obj = Broker(user_email, index_group_name).BrokerObject
        user_data = Configuration.objects.filter(user_id=user_email, index_name="nifty")
        config_dict = list(user_data.values())[0]
        print("values Generated")
        print(config_dict)
        checker = HighFrequencyTrading(index_name="nifty", user_email=user_email, BrokerObject=broker_obj)
        checker.startHFT()
    return JsonResponse({"started":"abc"}, safe=False)
