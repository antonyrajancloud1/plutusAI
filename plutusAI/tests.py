from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .server.broker.AngelOneBroker import AngelOneBroker
from .server.manualOrder import *
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
import time

@require_http_methods(["GET"])
def tester(request):
    try:
        user_email = "antonyrajan.d@gmail.com"
        user_broker_data = BrokerDetails.objects.filter(
            user_id=ADMIN_USER_ID, index_group=INDIAN_INDEX
        )
        BrokerObject = AngelOneBroker(user_broker_data)

        correlation_id = "admin_ws"
        trading_symbols = ["NIFTY12JUN2524650CE","NIFTY12JUN2524800PE"]
        tokens_for_candle = [BrokerObject.getTokenForSymbol(sym) for sym in trading_symbols]
        symbol_token_map =[{"symbol":trading_symbols[0],"token":tokens_for_candle[0]},{"symbol":trading_symbols[1],"token":tokens_for_candle[1]}]
        all_token_list = [{"exchangeType": 2, "tokens": tokens_for_candle}]
        print(all_token_list)

        # 🟡 Per-token tracking
        trade_states = {
            token: {
                "price_data": [],
                "position": None,
                "entry_price": None,
                "net_total_pnl": 0,
                "buyCompleted": False
            }
            for token in tokens_for_candle
        }

        def on_open(wsapp):
            addLogDetails(INFO, f"[WebSocket] Connection opened. Subscribing to tokens: {all_token_list}")
            sws.subscribe(correlation_id, 3, all_token_list)

        def on_data(wsapp, message):
            try:
                token = message["token"]
                symbol = next((item["symbol"] for item in symbol_token_map if item["token"] == token), None)
                if not symbol:
                    print(f"[{token}] No matching symbol found!")
                    return

                buyValue = message["best_5_buy_data"][0]["price"] / 100
                sellValue = message["best_5_sell_data"][0]["price"] / 100
                buyVolume = message["best_5_buy_data"][0]["quantity"]
                sellVolume = message["best_5_sell_data"][0]["quantity"]

                if token not in trade_states:
                    trade_states[token] = {
                        "price_data": [],
                        "position": None,
                        "entry_price": None,
                        "net_total_pnl": 0.0,
                        "buyCompleted": False,
                        "baseValue": None
                    }

                ts = trade_states[token]

                ts["price_data"].append({
                    "buy": buyValue,
                    "sell": sellValue,
                    "buyVol": buyVolume,
                    "sellVol": sellVolume
                })

                if len(ts["price_data"]) > 2:
                    ts["price_data"].pop(0)

                if len(ts["price_data"]) == 2:
                    first = ts["price_data"][0]
                    second = ts["price_data"][1]

                    if not ts["buyCompleted"]:
                        if second["buy"] > first["buy"]:
                            # 🟢 BUY Signal
                            ts["position"] = "LONG"
                            ts["entry_price"] = second["buy"]
                            ts["buyCompleted"] = True
                            ts["baseValue"] = first["buy"]
                            print(f"[{token}] BUY for {symbol} at {second['buy']:.2f} (Base: {ts['baseValue']:.2f})")

                            data = {
                                USER_ID: user_email,
                                SCRIPT_NAME: symbol,
                                QTY: 75,
                                ENTRY_PRICE: second["buy"],
                                STATUS: ORDER_PLACED,
                                STRATEGY: "Flash",
                                INDEX_NAME: "nifty"
                            }
                            addOrderBookDetails(data, True)
                        else:
                            print(f"[{token}] No trade condition met for {symbol}. HOLD.")
                    else:
                        # 🟢 Update trailing baseValue
                        ts["baseValue"] = first["buy"]

                        # 🟢 Check for exit
                        if second["buy"] < ts["baseValue"]:
                            # 🟢 EXIT
                            exit_data = {
                                EXIT_TIME: getCurrentTimestamp()
                            }
                            user_data = OrderBook.objects.filter(
                                user_id=user_email,
                                strategy="Flash",
                                script_name=symbol,
                                exit_price=None
                            )
                            order_info = user_data.values().first()
                            if order_info:
                                entry_price = order_info.get(ENTRY_PRICE)
                                pnl = (float(sellValue) - float(entry_price)) * 75
                                exit_data.update({
                                    TOTAL: str(pnl),
                                    EXIT_PRICE: sellValue,
                                    STATUS: ORDER_EXITED
                                })
                                user_data.update(**exit_data)

                                pnl_local = sellValue - ts["entry_price"]
                                ts["net_total_pnl"] += pnl_local
                                print(
                                    f"[{token}] EXIT for {symbol} at {sellValue:.2f}, PnL: {pnl_local:.2f}, Net PnL: {ts['net_total_pnl']:.2f}")

                            ts["position"] = None
                            ts["entry_price"] = None
                            ts["buyCompleted"] = False
                            ts["baseValue"] = None
                        else:
                            print(
                                f"[{token}] HOLD for {symbol}. Current Buy: {second['buy']:.2f}, Trailing Base: {ts['baseValue']:.2f}")

                    print("====================\n")

            except Exception as e:
                addLogDetails(ERROR, f"[on_data] Error for token {message.get('token')}: {e}")

        def on_error(wsapp, error):
            addLogDetails(ERROR, f"[WebSocket] Error: {error}")

        def on_close(wsapp):
            addLogDetails(INFO, "[WebSocket] Connection closed.")

        def create_websocket():
            ws = SmartWebSocketV2(
                BrokerObject.auth_token,
                BrokerObject.broker_api_token,
                BrokerObject.broker_user_id,
                BrokerObject.feed_token,
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

    except Exception as main_e:
        addLogDetails(ERROR, f"[Main Task Error] {main_e}")

    return JsonResponse({}, safe=False)
