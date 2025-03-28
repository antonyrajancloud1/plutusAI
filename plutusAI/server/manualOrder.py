from plutusAI.models import IndexDetails
from plutusAI.server.base import *
from plutusAI.server.broker.Broker import Broker
from plutusAI.server.constants import *

def placeManualOrder(user_email, user_index_data, OrderType):
    try:
        # Validate input data
        required_fields = [INDEX_NAME, STRIKE, LOTS, TARGET, STOP_LOSS]
        if not all(field in user_index_data for field in required_fields):
            error_msg = f"Missing required fields in user_index_data: {required_fields}"
            addLogDetails(ERROR, error_msg)
            return JsonResponse({STATUS: FAILED, MESSAGE: error_msg, TASK_STATUS: False})

        # Extract and validate data
        index_name = user_index_data[INDEX_NAME]
        strike = int(user_index_data[STRIKE])
        qty = int(user_index_data[LOTS])
        target = int(user_index_data[TARGET])
        stop_loss = int(user_index_data[STOP_LOSS])

        # Fetch index details
        index_data = IndexDetails.objects.filter(index_name=index_name).values()
        if not index_data:
            error_msg = f"Index data not found for {index_name}"
            addLogDetails(ERROR, error_msg)
            return JsonResponse({STATUS: FAILED, MESSAGE: error_msg, TASK_STATUS: False})
        index_qty = int(index_data[0].get(QTY, 0))
        user_qty = qty * index_qty

        # Initialize broker object
        broker = Broker(user_email, INDIAN_INDEX).BrokerObject

        # Calculate trading symbol
        if OrderType not in ["CE", "PE"]:
            error_msg = "Invalid OrderType provided. Must be 'CE' or 'PE'."
            addLogDetails(ERROR, error_msg)
            return JsonResponse({STATUS: FAILED, MESSAGE: error_msg, TASK_STATUS: False})

        atm = broker.getCurrentAtm(index_name)
        trading_symbol = f"{getTradingSymbol(index_name)}{atm - strike if OrderType == 'CE' else atm + strike}{OrderType}"

        # Fetch current premium details
        option_details = broker.getCurrentPremiumDetails(NFO, trading_symbol)
        ltp = broker.getLtpForPremium(option_details)

        # Check if current_premium is valid
        current_premium = getManualOrderDetails(user_email, index_name).get("current_premium")
        if current_premium:  # Proceed only if current_premium is valid
            try:
                # Validate if current_premium is a valid symbol
                token = broker.getTokenForSymbol(current_premium)
                if not token:
                    addLogDetails(INFO, f"Invalid current_premium: {current_premium}. Skipping sell order.")
                else:
                    # Place sell order for existing position
                    sell_order_details = {
                        VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: current_premium,
                        SYMBOL_TOKEN: token,
                        TRANSACTION_TYPE: SELL, ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY,
                        DURATION: DAY, QUANTITY: user_qty
                    }
                    addLogDetails(INFO, f"Placing sell order for current_premium: {current_premium}")
                    sell_order_response = broker.placeOrder(sell_order_details)
                    addLogDetails(INFO, f"Sell order response: {sell_order_response}")
            except Exception as e:
                error_msg = f"Error in selling previous order: {str(e)}"
                addLogDetails(ERROR, error_msg)
                # Continue to place the buy order even if sell order fails
        else:
            addLogDetails(INFO, "No valid current_premium found. Skipping sell order.")

        # Place buy order
        buy_order_details = {
            VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: trading_symbol,
            SYMBOL_TOKEN: broker.getTokenForSymbol(trading_symbol),
            TRANSACTION_TYPE: BUY, ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY,
            DURATION: DAY, QUANTITY: user_qty
        }
        addLogDetails(INFO, f"Placing buy order for trading_symbol: {trading_symbol}")
        order_response = broker.placeOrder(buy_order_details)
        addLogDetails(INFO, f"Buy order response: {order_response}")

        # Update order details
        updateManualOrderDetails(user_email, index_name, {
            "current_premium": trading_symbol,
            "order_id": order_response.get("data", {}).get("orderid"),
            "unique_order_id": order_response.get("data", {}).get("uniqueorderid")
        })

        return JsonResponse({STATUS: SUCCESS, MESSAGE: f"Order placed successfully {trading_symbol}", TASK_STATUS: True})

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        addLogDetails(ERROR, error_msg)
        return JsonResponse({STATUS: FAILED, MESSAGE: error_msg, TASK_STATUS: False})

def triggerOrder(user_email, user_index_data, strategy, order_type):
    try:
        print(user_email, user_index_data, strategy, order_type)
        strategy = strategy or "DefaultStrategy"

        index_name = user_index_data.get(INDEX_NAME)
        strike = int(user_index_data.get(STRIKE, 0))
        qty = int(user_index_data.get(LOTS, 0))

        index_data = IndexDetails.objects.filter(index_name=index_name).values().first()
        if not index_data:
            error_msg = f"Index data not found for {index_name}"
            addLogDetails(ERROR, error_msg)
            return JsonResponse({STATUS: FAILED, MESSAGE: error_msg, TASK_STATUS: False})

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
                        TOTAL: str((float(ltp) - float(entry_price)) * int(qty)),
                        EXIT_PRICE: ltp,
                        STATUS: ORDER_EXITED
                    })
                else:
                    print("Sell order")
                    exit_data = {INDEX_NAME: index_name,STRATEGY:strategy}

                    exitOrderWebhook(strategy, exit_data, user_email)
                user_data.update(**order_info)
            else:
                return JsonResponse(
                    {STATUS: SUCCESS, MESSAGE: f"{order_type.capitalize()} order already exists", TASK_STATUS: True})

        # Determine option type and strike logic
        option_type = CE if order_type.upper() == BUY else PE
        strike_price = atm - strike if order_type.upper() == BUY else atm + strike
        trading_symbol = f"{getTradingSymbol(index_name)}{strike_price}{option_type}"

        # Fetch current premium details
        option_details = broker.getCurrentPremiumDetails(NFO, trading_symbol)
        ltp = broker.getLtpForPremium(option_details)
        print(option_details)
        if broker.is_demo_enabled:
            option_buy_price = ltp
        else:
            # Get Candle Data

            from_time = str(get_previous_minute_start(get_current_minute_start(), False))
            to_time = str(get_next_minute_start_ms(get_current_minute_start(), False))
            print(from_time,to_time)
            # from_time = "2025-03-26 14:04"
            # to_time="2025-03-26 14:05"

            candle_data_df = broker.getCandleData(NFO, option_details[SYMBOL_TOKEN], from_time, to_time, "ONE_MINUTE")
            high_price = float(candle_data_df.loc[0, HIGH])

            # order_details=None
            if high_price is None or float(ltp) > high_price:

                ## Option Buying ##
                order_details = {
                    VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: trading_symbol,
                    SYMBOL_TOKEN: broker.getTokenForSymbol(trading_symbol),
                    TRANSACTION_TYPE: BUY ,
                    ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY,
                    DURATION: DAY, QUANTITY: user_qty
                }
            else:
                order_details= {
                    VARIETY: STOPLOSS, EXCHANGE: NFO, TRADING_SYMBOL: trading_symbol,
                    SYMBOL_TOKEN: broker.getTokenForSymbol(trading_symbol),
                    TRANSACTION_TYPE: BUY,
                    ORDER_TYPE: ORDER_TYPE_SL, PRODUCT_TYPE: INTRADAY,
                    DURATION: DAY, QUANTITY: user_qty,TRIGGER_PRICE:high_price,PRICE:high_price
                }
            print("#############")
            print(ltp)
            print(high_price)
            print(order_details)
            print("#############")
            addLogDetails(INFO, f"Placing {order_type.lower()} order for {trading_symbol}")
            order_response = broker.placeOrder(order_details)
            addLogDetails(INFO, f"{order_type.capitalize()} order response: {order_response}")

            unique_order_id = order_response.get("data", {}).get("uniqueorderid")
            order_response_details = broker.getOrderDetails(unique_order_id)
            option_buy_price = order_response_details.get("averageprice", ltp)  # Fallback to LTP

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
        return JsonResponse(
            {STATUS: SUCCESS, MESSAGE: f"{order_type.capitalize()} order placed successfully", TASK_STATUS: True})

    except Exception as e:
        error_msg = f"Unexpected error in trigger_order: {str(e)}"
        addLogDetails(ERROR, error_msg)
        return JsonResponse({STATUS: FAILED, MESSAGE: error_msg, TASK_STATUS: False})


def exitOrderWebhook(strategy, data, user_email):
    try:
        data[EXIT_TIME] = getCurrentTimestamp()
        broker = Broker(user_email, INDIAN_INDEX).BrokerObject

        user_data = OrderBook.objects.filter(
            user_id=user_email, strategy=strategy, exit_price=None
        )

        if user_data.exists():
            order_info = user_data.values().first()
            entry_price = order_info[ENTRY_PRICE]
            qty = order_info[QTY]
            script_name = order_info[SCRIPT_NAME]

            if broker.is_demo_enabled:
                option_details = broker.getCurrentPremiumDetails(NFO, script_name)
                ltp = broker.getLtpForPremium(option_details)
                data.update({
                    TOTAL: str((float(ltp) - float(entry_price)) * int(qty)),
                    EXIT_PRICE: ltp,
                    STATUS:ORDER_EXITED
                })
            else:
                user_webkook_data = WebhookDetails.objects.filter(user_id=user_email, index_name=data[INDEX_NAME],
                                                                  strategy=strategy)
                user_webkook_data= list(user_webkook_data.values())[0]
                trading_symbol = user_webkook_data[CURRENT_PREMIUM]
                print("EXIT")
                print(broker.smartApi.position())
                print(broker.checkIfOrderExists(user_webkook_data[UNIQUE_ORDER_ID]))
                if broker.checkIfOrderPlaced(user_webkook_data[UNIQUE_ORDER_ID]):
                    order_details = {
                        VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: trading_symbol,
                        SYMBOL_TOKEN: broker.getTokenForSymbol(trading_symbol),
                        TRANSACTION_TYPE: SELL,
                        ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY,
                        DURATION: DAY, QUANTITY: qty
                    }
                    order_response = broker.placeOrder(order_details)
                    print(order_response)
                elif broker.checkIfOrderExists(user_webkook_data[UNIQUE_ORDER_ID]):
                    broker.cancelOrder(user_webkook_data[ORDER_ID],NORMAL)
            user_data.update(**data)
            return JsonResponse({STATUS: SUCCESS, MESSAGE: "Order Exited", TASK_STATUS: True})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: f"No Pending orders for strategy {strategy}", TASK_STATUS: True})

    except Exception as e:
        error_msg = f"Unexpected error in exit_order_webhook: {str(e)}"
        addLogDetails(ERROR, error_msg)
        return JsonResponse({STATUS: FAILED, MESSAGE: error_msg, TASK_STATUS: False})
