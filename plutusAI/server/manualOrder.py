from plutusAI.server.base import *
from plutusAI.server.broker.Broker import Broker
from plutusAI.server.constants import *


def triggerOrder(user_email, user_index_data, strategy, order_type):
    try:
        strategy = strategy or "DefaultStrategy"

        index_name = user_index_data.get(INDEX_NAME)
        strike = int(user_index_data.get(STRIKE, 0))
        qty = int(user_index_data.get(LOTS, 0))
        on_candle_close = bool(user_index_data.get(ON_CANDLE_CLOSE))
        product_type = user_index_data.get(PRODUCT_TYPE)
        timeframe = user_index_data.get(TIMEFRAME)


        index_data = IndexDetails.objects.filter(index_name=index_name).values().first()
        if not index_data:
            error_msg = f"Index data not found for {index_name}"
            addLogDetails(ERROR, error_msg)
            return JsonResponse({STATUS: FAILED, MESSAGE: "error_msg", TASK_STATUS: False})

        index_qty = int(index_data.get(QTY, 0))
        user_qty = qty * index_qty
        broker = Broker(user_email, INDIAN_INDEX).BrokerObject
        atm = broker.getCurrentAtm(index_name)
        # Exit order handling
        user_data = OrderBook.objects.filter(
            user_id=user_email, strategy=strategy, exit_price=None
        )

        if user_data.exists():
            order_info = user_data.values().first()
            script_name = order_info[SCRIPT_NAME]

            if (order_type == BUY and PE in script_name.upper()) or (order_type == SELL and CE in script_name.upper()):
                order_info[EXIT_TIME] = getCurrentTimestamp()
                entry_price = order_info[ENTRY_PRICE]

                if broker.is_demo_enabled:
                    option_details = broker.getCurrentPremiumDetails(NFO, script_name)
                    ltp = broker.getLtpForPremium(option_details)
                    order_info.update({
                        TOTAL: str((float(ltp) - float(entry_price)) * int(user_qty)),
                        EXIT_PRICE: ltp,
                        STATUS: ORDER_EXITED
                    })
                    user_data.update(**order_info)
                else:
                    addLogDetails(INFO, "Sell order")
                    exit_data = {INDEX_NAME: index_name,STRATEGY:strategy}

                    exitOrderWebhook(strategy, exit_data, user_email)
                # user_data.update(**order_info)
            else:
                addLogDetails(INFO,f"{order_type.capitalize()} order already exists")
                return JsonResponse({STATUS: SUCCESS, MESSAGE: "Message Exists" , TASK_STATUS: True})




        # Determine option type and strike logic
        option_type = CE if order_type.upper() == BUY else PE
        strike_price = atm - strike if order_type.upper() == BUY else atm + strike
        trading_symbol = f"{getTradingSymbol(index_name)}{strike_price}{option_type}"
        # Fetch current premium details
        option_details = broker.getCurrentPremiumDetails(NFO, trading_symbol)
        ltp = broker.getLtpForPremium(option_details)
        addLogDetails(INFO,option_details)
        if broker.is_demo_enabled:
            option_buy_price = ltp
        else:
            if on_candle_close:
                TIMEFRAME_TO_MINUTES = {
                    "ONE_MINUTE": 1,
                    "THREE_MINUTE": 3,
                    "FIVE_MINUTE": 5,
                    "TEN_MINUTE": 10,
                    "FIFTEEN_MINUTE": 15,
                    "THIRTY_MINUTE": 30,
                    "ONE_HOUR": 60,
                    "ONE_DAY": 1440
                }
                minutes = TIMEFRAME_TO_MINUTES.get(timeframe, 6)
                from_time = str(get_previous_n_minute_start(get_current_minute_start(), False, minutes+1))
                to_time = str(get_next_minute_start_ms(get_current_minute_start(), False))
                addLogDetails(INFO, "Get Candle Details")
                addLogDetails(INFO, f"from_time: {from_time}")
                addLogDetails(INFO, f"to_time: {to_time}")
                try:
                    candle_data_df = broker.getCandleData(NFO,option_details[SYMBOL_TOKEN],from_time,to_time,timeframe)
                    if not candle_data_df.empty and HIGH in candle_data_df.columns:
                        high_price = float(candle_data_df.loc[0, HIGH])
                        addLogDetails(INFO, f"High Price: {high_price}")

                        if float(ltp) < high_price:
                            trigger = round(high_price * 1.001, 1)  # slight buffer
                            order_details = {
                                VARIETY: STOPLOSS, EXCHANGE: NFO, TRADING_SYMBOL: trading_symbol,
                                SYMBOL_TOKEN: broker.getTokenForSymbol(trading_symbol),
                                TRANSACTION_TYPE: BUY,
                                ORDER_TYPE: ORDER_TYPE_SL, PRODUCT_TYPE: product_type,
                                DURATION: DAY, QUANTITY: user_qty,
                                TRIGGER_PRICE: trigger, PRICE: trigger
                            }
                        else:
                            order_details = {
                                VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: trading_symbol,
                                SYMBOL_TOKEN: broker.getTokenForSymbol(trading_symbol),
                                TRANSACTION_TYPE: BUY,
                                ORDER_TYPE: MARKET, PRODUCT_TYPE: product_type,
                                DURATION: DAY, QUANTITY: user_qty
                            }
                    else:
                        addLogDetails(ERROR, "Candle data missing or HIGH column not found. Using market order.")
                        order_details = {
                            VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: trading_symbol,
                            SYMBOL_TOKEN: broker.getTokenForSymbol(trading_symbol),
                            TRANSACTION_TYPE: BUY,
                            ORDER_TYPE: MARKET, PRODUCT_TYPE: product_type,
                            DURATION: DAY, QUANTITY: user_qty
                        }

                except Exception as e:
                    addLogDetails(ERROR, f"Error fetching candle data: {str(e)}. Using market order.")
                    order_details = {
                        VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: trading_symbol,
                        SYMBOL_TOKEN: broker.getTokenForSymbol(trading_symbol),
                        TRANSACTION_TYPE: BUY,
                        ORDER_TYPE: MARKET, PRODUCT_TYPE: product_type,
                        DURATION: DAY, QUANTITY: user_qty
                    }

            else:
                order_details = {
                    VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: trading_symbol,
                    SYMBOL_TOKEN: broker.getTokenForSymbol(trading_symbol),
                    TRANSACTION_TYPE: BUY,
                    ORDER_TYPE: MARKET, PRODUCT_TYPE: product_type,
                    DURATION: DAY, QUANTITY: user_qty
                }

            addLogDetails(INFO, f"Placing {order_type.lower()} order for {trading_symbol}")
            order_response = broker.placeOrder(order_details)
            addLogDetails(INFO, f"{order_type.capitalize()} order response: {order_response}")
            unique_order_id = order_response.get("data", {}).get("uniqueorderid")
            order_response_details = broker.getOrderDetails(unique_order_id)
            if str(order_details.get(ORDER_TYPE)).__eq__(MARKET):
                option_buy_price = order_response_details.get("price", ltp)  # Fallback to LTP
            else:
                option_buy_price = order_response_details.get("triggerprice", ltp)
            addWebhookOrderDetails(user_email, index_name, strategy,{
                "current_premium": trading_symbol,
                "order_id": order_response.get("data", {}).get("orderid"),
                "unique_order_id": unique_order_id
            })

        data = {
            USER_ID: user_email, SCRIPT_NAME: trading_symbol, QTY: user_qty,
            ENTRY_PRICE: option_buy_price, STATUS: ORDER_PLACED, STRATEGY: strategy,
            INDEX_NAME: index_name
        }

        addOrderBookDetails(data, True)
        addLogDetails(INFO,f"{order_type.capitalize()} order placed successfully")
        return JsonResponse(
            {STATUS: SUCCESS, MESSAGE: "Message Exits", TASK_STATUS: True})

    except Exception as e:
        error_msg = f"Unexpected error in trigger_order: {str(e)}"
        addLogDetails(ERROR, error_msg)
        return JsonResponse({STATUS: FAILED, MESSAGE: "Unexpected error Check logs", TASK_STATUS: False})



def exitOrderWebhook(strategy, data, user_email):
    try:
        exit_data={}
        exit_data[EXIT_TIME] = getCurrentTimestamp()
        broker = Broker(user_email, INDIAN_INDEX).BrokerObject

        user_data = OrderBook.objects.filter(
            user_id=user_email, strategy=strategy, exit_price=None
        )
        if not user_data.exists():
            addLogDetails(INFO, f"No Pending orders for strategy {strategy}")
            return JsonResponse({STATUS: FAILED, MESSAGE: "No pending Messages", TASK_STATUS: False})

        index_name = data.get(INDEX_NAME)
        user_manual_details = ManualOrders.objects.filter(user_id=user_email, index_name=index_name)
        product_type = user_manual_details.values().first()[PRODUCT_TYPE]
        order_info = user_data.values().first()
        entry_price = order_info.get(ENTRY_PRICE)
        qty = order_info.get(QTY)
        script_name = order_info.get(SCRIPT_NAME)

        option_details = broker.getCurrentPremiumDetails(NFO, script_name)
        ltp = broker.getLtpForPremium(option_details)

        if broker.is_demo_enabled:
            exit_data.update({
                TOTAL: str((float(ltp) - float(entry_price)) * int(qty)),
                EXIT_PRICE: ltp,
                STATUS: ORDER_EXITED
            })
            user_data.update(**exit_data)
        else:
            user_webhook_data = WebhookDetails.objects.filter(
                user_id=user_email, index_name=data[INDEX_NAME], strategy=strategy
            )

            if not user_webhook_data.exists():
                addLogDetails(INFO, f"No webhook data found for {strategy}")
                return JsonResponse({STATUS: FAILED, MESSAGE: "No webhook data found", TASK_STATUS: False})

            user_webhook_data = user_webhook_data.values().first()
            trading_symbol = user_webhook_data.get(CURRENT_PREMIUM)
            unique_order_id = user_webhook_data.get(UNIQUE_ORDER_ID)

            if broker.checkIfOrderPlaced(unique_order_id):
                order_details = {
                    VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: trading_symbol,
                    SYMBOL_TOKEN: broker.getTokenForSymbol(trading_symbol),
                    TRANSACTION_TYPE: SELL, ORDER_TYPE: MARKET, PRODUCT_TYPE: product_type,
                    DURATION: DAY, QUANTITY: qty
                }

                order_response_details = broker.placeOrder(order_details)
                addLogDetails(INFO, f"Order placed: {order_response_details}")

                option_exit_price = order_response_details.get("price") or ltp
                exit_data.update({
                    TOTAL: str((float(option_exit_price) - float(entry_price)) * int(qty)),
                    EXIT_PRICE: option_exit_price,
                    STATUS: ORDER_EXITED
                })
                user_data.update(**exit_data)
            elif broker.checkIfOrderExists(unique_order_id):
                broker.cancelOrder(user_webhook_data.get(ORDER_ID), NORMAL)
                addLogDetails(INFO, "Existing order cancelled.")
                user_data.delete()
            else:
                addLogDetails(INFO, "Order status not found so deleting entry.")
                user_data.delete()
        # user_data.update(**data)
        addLogDetails(INFO, "Order exited successfully.")
        return JsonResponse({STATUS: SUCCESS, MESSAGE: "Message Done", TASK_STATUS: True})

    except Exception as e:
        error_msg = f"Unexpected error in exit_order_webhook: {repr(e)}"
        addLogDetails(ERROR, error_msg)
        return JsonResponse({STATUS: FAILED, MESSAGE: "Unexpected error. Check logs.", TASK_STATUS: False})


def modifyToMarketOrder(user_email, user_index_data, strategy, order_type):
    try:
        broker = Broker(user_email, INDIAN_INDEX).BrokerObject
        index_name = user_index_data.get(INDEX_NAME)
        user_manual_details = ManualOrders.objects.filter(user_id=user_email, index_name=index_name)
        product_type = user_manual_details.values().first()[PRODUCT_TYPE]

        if not  broker.is_demo_enabled:

            user_data = OrderBook.objects.filter(
                user_id=user_email, strategy=strategy, exit_price=None
            )
            if not user_data.exists():
                addLogDetails(INFO, f"No Pending orders for strategy {strategy}")
                return JsonResponse({STATUS: FAILED, MESSAGE: "No pending Messages", TASK_STATUS: False})

            order_info = user_data.values().first()
            qty = order_info.get(QTY)


            user_webhook_data = WebhookDetails.objects.filter(
                user_id=user_email, index_name=index_name, strategy=strategy
            ).values().first()

            if not user_webhook_data:
                error_msg = f"Webhook details not found for {user_email}, strategy: {strategy}"
                addLogDetails(ERROR, error_msg)
                return JsonResponse({STATUS: FAILED, MESSAGE: error_msg, TASK_STATUS: False})

            index_data = IndexDetails.objects.filter(index_name=index_name).values()
            if not index_data:
                error_msg = f"Index data not found for {index_name}"
                addLogDetails(ERROR, error_msg)
                return JsonResponse({STATUS: FAILED, MESSAGE: error_msg, TASK_STATUS: False})

            index_qty = int(index_data[0].get(QTY, 0))
            user_qty = qty * index_qty

            trading_symbol = user_webhook_data.get(CURRENT_PREMIUM)
            unique_order_id = user_webhook_data.get(UNIQUE_ORDER_ID)

            if broker.checkIfOrderPlaced(unique_order_id):
                msg = f"Order already placed for ID {unique_order_id}"
                addLogDetails(INFO, msg)
                return JsonResponse({STATUS: SUCCESS, MESSAGE: msg, TASK_STATUS: True})

            order_details = {
                VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: trading_symbol,
                SYMBOL_TOKEN: broker.getTokenForSymbol(trading_symbol),
                TRANSACTION_TYPE: BUY, ORDER_TYPE: MARKET, PRODUCT_TYPE: product_type,
                DURATION: DAY, QUANTITY: user_qty
            }

            order_response_details = broker.placeOrder(order_details)
            addLogDetails(INFO, f"Order placed: {order_response_details}")

            option_buy_price = order_response_details.get("averageprice")
            data = {
                USER_ID: user_email, SCRIPT_NAME: trading_symbol, QTY: user_qty,
                ENTRY_PRICE: option_buy_price, STATUS: ORDER_PLACED, STRATEGY: strategy,
                INDEX_NAME: index_name
            }

            addOrderBookDetails(data, True)

            return JsonResponse( {STATUS: SUCCESS, MESSAGE: "Order placed successfully", TASK_STATUS: True})
        else:
            return JsonResponse({STATUS: SUCCESS, MESSAGE: "Demo Enabled", TASK_STATUS: True})

    except Exception as e:
        error_msg = f"Unexpected error in modifyToMarketOrder: {str(e)}"
        addLogDetails(ERROR, error_msg)
        return JsonResponse({STATUS: FAILED, MESSAGE: "Unexpected error. Check logs.", TASK_STATUS: False})
