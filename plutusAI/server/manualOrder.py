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
    print(user_email, user_index_data, strategy, order_type)
    strategy = strategy if strategy else "DefaultStrategy"

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
    print("before broker")
    broker = Broker(user_email, INDIAN_INDEX).BrokerObject
    print("After broker")
    atm = broker.getCurrentAtm(index_name)
    print(atm)
    # Determine option type and strike logic
    if order_type.upper() == BUY:
        option_type = "CE"
        strike_price = atm - strike  # Call Option (CE) -> atm - strike
    elif order_type.upper() == SELL:
        option_type = "PE"
        strike_price = atm + strike  # Put Option (PE) -> atm + strike
    else:
        error_msg = f"Invalid order type: {order_type}"
        addLogDetails(ERROR, error_msg)
        return JsonResponse({STATUS: FAILED, MESSAGE: error_msg, TASK_STATUS: False})

    trading_symbol = f"{getTradingSymbol(index_name)}{strike_price}{option_type}"

    # Fetch current premium details
    option_details = broker.getCurrentPremiumDetails(NFO, trading_symbol)
    ltp = broker.getLtpForPremium(option_details)
    print(option_details)
    if broker.is_demo_enabled:
        print("into demo")
        optionBuyPrice = ltp
        data = {
            USER_ID: user_email, SCRIPT_NAME: trading_symbol, QTY: qty,
            ENTRY_PRICE: optionBuyPrice, STATUS: ORDER_PLACED, STRATEGY: strategy,
            INDEX_NAME: index_name
        }
    else:
        order_details = {
            VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: trading_symbol,
            SYMBOL_TOKEN: broker.getTokenForSymbol(trading_symbol),
            TRANSACTION_TYPE: BUY if order_type.upper() == BUY else SELL,
            ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY,
            DURATION: DAY, QUANTITY: user_qty
        }

        addLogDetails(INFO, f"Placing {order_type.lower()} order for {trading_symbol}")
        order_response = broker.placeOrder(order_details)
        addLogDetails(INFO, f"{order_type.capitalize()} order response: {order_response}")

        uniqueorderid = order_response.get("data", {}).get("uniqueorderid")
        order_response_details = broker.getOrderDetails(uniqueorderid)

        optionBuyPrice = order_response_details.get("averageprice", ltp)  # Fallback to LTP if missing
        data = {
            USER_ID: user_email, SCRIPT_NAME: trading_symbol, QTY: qty,
            ENTRY_PRICE: optionBuyPrice, STATUS: ORDER_PLACED, STRATEGY: strategy,
            INDEX_NAME: index_name
        }

        # Update order details
        updateManualOrderDetails(user_email, index_name, {
            "current_premium": trading_symbol,
            "order_id": order_response.get("data", {}).get("orderid"),
            "unique_order_id": uniqueorderid
        })

    addOrderBookDetails(data, True)
    return JsonResponse({STATUS: SUCCESS, MESSAGE: f"{order_type.capitalize()} order placed successfully", TASK_STATUS: True})

def exitOrderWebhook(strategy,data):
    try:
        print(strategy)
        current_time_str = getCurrentTimestamp()
        data[EXIT_TIME] = current_time_str
        broker = Broker(data[USER_ID], INDIAN_INDEX).BrokerObject


        user_data = OrderBook.objects.filter(
            user_id=data[USER_ID], strategy=strategy, exit_price=None
        )
        order_info = list(user_data.values())[0]
        entry_price = order_info[ENTRY_PRICE]
        exit_price = data[EXIT_PRICE]
        qty = order_info[QTY]
        script_name=order_info[SCRIPT_NAME]
        if broker.is_demo_enabled:
            option_details = broker.getCurrentPremiumDetails(NFO, script_name)
            ltp = broker.getLtpForPremium(option_details)
            total = str(float((float(exit_price) - float(entry_price)) * int(qty)))
            data[TOTAL] = total
        else:
            print("sell order")
        user_data.update(**data)
        return JsonResponse({STATUS: FAILED, MESSAGE: "Order Exited", TASK_STATUS: True})
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        addLogDetails(ERROR, error_msg)
        return JsonResponse({STATUS: FAILED, MESSAGE: error_msg, TASK_STATUS: False})
