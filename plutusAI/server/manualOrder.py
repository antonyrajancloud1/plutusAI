from plutusAI.models import IndexDetails
from plutusAI.server.base import *
from plutusAI.server.broker.Broker import Broker
from plutusAI.server.constants import *


# def placeManualOrder(user_email, user_index_data, OrderType):
#     try:
#
#         index_name = user_index_data.get(INDEX_NAME)
#         strike = user_index_data.get(STRIKE)
#         qty = int(user_index_data.get(LOTS))
#         target = int(user_index_data.get(TARGET))
#         stop_loss = int(user_index_data.get(STOP_LOSS))
#         index_data = IndexDetails.objects.filter(index_name=index_name).values()
#         manual_order_details = getManualOrderDetails(user_email, index_name)
#         if not index_data:
#             raise ValueError(f"Index data not found for {index_name}")
#         current_premium = manual_order_details.get("current_premium")
#         index_qty = int(index_data[0].get(QTY, 0))
#         user_qty = qty * index_qty
#         BrokerObject = Broker(user_email, INDIAN_INDEX).BrokerObject
#         if OrderType == "CE":
#             currentPremiumPlaced = f"{getTradingSymbol(index_name)}{BrokerObject.getCurrentAtm(index_name) - int(strike)}CE"
#         elif OrderType == "PE":
#             currentPremiumPlaced = f"{getTradingSymbol(index_name)}{BrokerObject.getCurrentAtm(index_name) + int(strike)}PE"
#         else:
#             raise ValueError("Invalid OrderType provided. Must be 'CE' or 'PE'.")
#
#         optionDetails = BrokerObject.getCurrentPremiumDetails(NFO, currentPremiumPlaced)
#         addLogDetails(INFO,optionDetails)
#         ltpDetails = BrokerObject.getLtpForPremium(optionDetails)
#
#         trigger_price = round(float(ltpDetails), 1)+float(user_index_data.get("trigger"))
#         price = trigger_price
#         #target = price+target
#         stop_loss=price-stop_loss
#
#         # buy_order_details = {
#         #     VARIETY: STOPLOSS,
#         #     EXCHANGE: NFO,
#         #     TRADING_SYMBOL: currentPremiumPlaced,
#         #     SYMBOL_TOKEN: BrokerObject.getTokenForSymbol(currentPremiumPlaced),
#         #     TRANSACTION_TYPE: BUY,
#         #     ORDER_TYPE: ORDER_TYPE_SL,
#         #     PRICE: price,
#         #     TRIGGER_PRICE: trigger_price,
#         #     PRODUCT_TYPE: INTRADAY,
#         #     DURATION: DAY,
#         #     QUANTITY: user_qty
#         # }
#
#         # buy_order_details = {
#         #     VARIETY: "ROBO",
#         #     EXCHANGE: NFO,
#         #     TRADING_SYMBOL: currentPremiumPlaced,
#         #     SYMBOL_TOKEN: BrokerObject.getTokenForSymbol(currentPremiumPlaced),
#         #     TRANSACTION_TYPE: BUY,
#         #     ORDER_TYPE: "LIMIT",
#         #     PRICE: price,
#         #     PRODUCT_TYPE: INTRADAY,
#         #     DURATION: DAY,
#         #     QUANTITY: user_qty,
#         #     "squareoff":target,
#         #     "stoploss":stop_loss,
#         # }
#         try:
#             sell_order_details = {VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: current_premium,
#                                  SYMBOL_TOKEN: BrokerObject.getTokenForSymbol(current_premium),
#                                  TRANSACTION_TYPE: SELL, ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY, DURATION: DAY,
#                                  QUANTITY: user_qty}
#             addLogDetails(INFO, sell_order_details)
#             sell_order_response = BrokerObject.placeOrder(sell_order_details)
#             addLogDetails(INFO, sell_order_response)
#             sell_order_response_data = sell_order_response.get("data", {})
#             addLogDetails(INFO,sell_order_response_data)
#         except Exception as e:
#             addLogDetails(ERROR, "Error in selling previous order")
#             addLogDetails(ERROR,str(e))
#
#         buy_order_details = {VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: currentPremiumPlaced,
#                              SYMBOL_TOKEN: BrokerObject.getTokenForSymbol(currentPremiumPlaced),
#                              TRANSACTION_TYPE: BUY, ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY, DURATION: DAY,
#                              QUANTITY: user_qty}
#         addLogDetails(INFO,buy_order_details)
#         order_response = BrokerObject.placeOrder(buy_order_details)
#
#
#
#
#         order_response_data = order_response.get("data", {})
#         data = {
#             "current_premium": order_response_data.get("script"),
#             "order_id": order_response_data.get("orderid"),
#             "unique_order_id": order_response_data.get("uniqueorderid")
#         }
#         addLogDetails(INFO, f"Manual Order placed UserId ={user_email} LTP while placing order : {ltpDetails} data = {buy_order_details}")
#         updateManualOrderDetails(user_email, index_name, data=data)
#         order_response_from_broker = BrokerObject.getOrderDetails(order_response_data.get("uniqueorderid"))
#         addLogDetails(INFO, "order_response_from_broker")
#         addLogDetails(INFO,order_response_from_broker)
#         #option_buy_price=order_response_from_broker["data"][""]
#         addLogDetails(INFO,f"Manual Order placed UserId ={user_email} data = {order_response}")
#         # exit_order_details = {VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: currentPremiumPlaced,
#         #                       SYMBOL_TOKEN: BrokerObject.getTokenForSymbol(currentPremiumPlaced),
#         #                       TRANSACTION_TYPE: SELL, ORDER_TYPE: ORDER_TYPE_LIMIT, PRODUCT_TYPE: INTRADAY, DURATION: DAY,
#         #                       QUANTITY: user_qty, PRICE: float(ltpDetails)+target}
#         # addLogDetails(INFO, exit_order_details)
#         # exit_order_response = BrokerObject.placeOrder(exit_order_details)
#         # addLogDetails(INFO, exit_order_response)
#         return JsonResponse({STATUS: SUCCESS, MESSAGE: str(order_response_from_broker), TASK_STATUS: True})
#
#     except Exception as e:
#         addLogDetails(ERROR,str(e))
#         return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR, TASK_STATUS: False})
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