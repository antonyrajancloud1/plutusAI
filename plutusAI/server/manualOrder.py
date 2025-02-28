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


from django.http import JsonResponse
from logging import ERROR, INFO

# Constants
BUY = "BUY"
SELL = "SELL"
CE = "CE"
PE = "PE"
NFO = "NFO"
ORDER_PLACED = "Order Placed"
MARKET = "MARKET"
INTRADAY = "INTRADAY"
DAY = "DAY"
NORMAL = "NORMAL"
SUCCESS = "Success"
FAILED = "Failed"


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
        user_index_data[EXIT_TIME] = getCurrentTimestamp()

        user_data = OrderBook.objects.filter(
            user_id=user_email, strategy=strategy, exit_price=None
        )

        if user_data.exists():
            order_info = user_data.values().first()
            entry_price = order_info[ENTRY_PRICE]
            script_name = order_info[SCRIPT_NAME]

            if broker.is_demo_enabled:
                option_details = broker.getCurrentPremiumDetails(NFO, script_name)
                ltp = broker.getLtpForPremium(option_details)
                user_index_data.update({
                    TOTAL: str((float(ltp) - float(entry_price)) * int(qty)),
                    EXIT_PRICE: ltp,
                    STATUS: ORDER_EXITED
                })
            else:
                print("Sell order")
            user_data.update(**user_index_data)
        else:
            addLogDetails(INFO,"No Orders present for exit")

        # Determine option type and strike logic
        option_type = CE if order_type.upper() == BUY else PE
        strike_price = atm - strike if order_type.upper() == BUY else atm + strike
        trading_symbol = f"{getTradingSymbol(index_name)}{strike_price}{option_type}"

        # Fetch current premium details
        option_details = broker.getCurrentPremiumDetails(NFO, trading_symbol)
        ltp = broker.getLtpForPremium(option_details)
        print(option_details)

        if broker.is_demo_enabled:
            print("Into demo mode")
            option_buy_price = ltp
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

            unique_order_id = order_response.get("data", {}).get("uniqueorderid")
            order_response_details = broker.getOrderDetails(unique_order_id)
            option_buy_price = order_response_details.get("averageprice", ltp)  # Fallback to LTP

            updateManualOrderDetails(user_email, index_name, {
                "current_premium": trading_symbol,
                "order_id": order_response.get("data", {}).get("orderid"),
                "unique_order_id": unique_order_id
            })

        data = {
            USER_ID: user_email, SCRIPT_NAME: trading_symbol, QTY: qty,
            ENTRY_PRICE: option_buy_price, STATUS: ORDER_PLACED, STRATEGY: strategy,
            INDEX_NAME: index_name
        }

        addOrderBookDetails(data, True)
        return JsonResponse({STATUS: SUCCESS, MESSAGE: f"{order_type.capitalize()} order placed successfully", TASK_STATUS: True})

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
                print("Sell order")
            user_data.update(**data)
            return JsonResponse({STATUS: SUCCESS, MESSAGE: "Order Exited", TASK_STATUS: True})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: f"No Pending orders for strategy {strategy}", TASK_STATUS: True})

    except Exception as e:
        error_msg = f"Unexpected error in exit_order_webhook: {str(e)}"
        addLogDetails(ERROR, error_msg)
        return JsonResponse({STATUS: FAILED, MESSAGE: error_msg, TASK_STATUS: False})