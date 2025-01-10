from plutusAI.models import IndexDetails
from plutusAI.server.base import *
from plutusAI.server.broker.Broker import Broker
from plutusAI.server.constants import *


def placeManualOrder(user_email, user_index_data, OrderType):
    try:

        index_name = user_index_data.get(INDEX_NAME)
        strike = user_index_data.get(STRIKE)
        qty = int(user_index_data.get(LOTS))
        target = int(user_index_data.get(TARGET))
        stop_loss = int(user_index_data.get(STOP_LOSS))
        index_data = IndexDetails.objects.filter(index_name=index_name).values()
        manual_order_details = getManualOrderDetails(user_email, index_name)
        if not index_data:
            raise ValueError(f"Index data not found for {index_name}")
        current_premium = manual_order_details.get("current_premium")
        index_qty = int(index_data[0].get(QTY, 0))
        user_qty = qty * index_qty
        BrokerObject = Broker(user_email, INDIAN_INDEX).BrokerObject
        if OrderType == "CE":
            currentPremiumPlaced = f"{getTradingSymbol(index_name)}{BrokerObject.getCurrentAtm(index_name) - int(strike)}CE"
        elif OrderType == "PE":
            currentPremiumPlaced = f"{getTradingSymbol(index_name)}{BrokerObject.getCurrentAtm(index_name) + int(strike)}PE"
        else:
            raise ValueError("Invalid OrderType provided. Must be 'CE' or 'PE'.")

        optionDetails = BrokerObject.getCurrentPremiumDetails(NFO, currentPremiumPlaced)
        addLogDetails(INFO,optionDetails)
        ltpDetails = BrokerObject.getLtpForPremium(optionDetails)

        trigger_price = round(float(ltpDetails), 1)+float(user_index_data.get("trigger"))
        price = trigger_price
        #target = price+target
        stop_loss=price-stop_loss

        # buy_order_details = {
        #     VARIETY: STOPLOSS,
        #     EXCHANGE: NFO,
        #     TRADING_SYMBOL: currentPremiumPlaced,
        #     SYMBOL_TOKEN: BrokerObject.getTokenForSymbol(currentPremiumPlaced),
        #     TRANSACTION_TYPE: BUY,
        #     ORDER_TYPE: ORDER_TYPE_SL,
        #     PRICE: price,
        #     TRIGGER_PRICE: trigger_price,
        #     PRODUCT_TYPE: INTRADAY,
        #     DURATION: DAY,
        #     QUANTITY: user_qty
        # }

        # buy_order_details = {
        #     VARIETY: "ROBO",
        #     EXCHANGE: NFO,
        #     TRADING_SYMBOL: currentPremiumPlaced,
        #     SYMBOL_TOKEN: BrokerObject.getTokenForSymbol(currentPremiumPlaced),
        #     TRANSACTION_TYPE: BUY,
        #     ORDER_TYPE: "LIMIT",
        #     PRICE: price,
        #     PRODUCT_TYPE: INTRADAY,
        #     DURATION: DAY,
        #     QUANTITY: user_qty,
        #     "squareoff":target,
        #     "stoploss":stop_loss,
        # }
        try:
            sell_order_details = {VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: current_premium,
                                 SYMBOL_TOKEN: BrokerObject.getTokenForSymbol(current_premium),
                                 TRANSACTION_TYPE: SELL, ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY, DURATION: DAY,
                                 QUANTITY: user_qty}
            addLogDetails(INFO, sell_order_details)
            sell_order_response = BrokerObject.placeOrder(sell_order_details)
            addLogDetails(INFO, sell_order_response)
            sell_order_response_data = sell_order_response.get("data", {})
            addLogDetails(INFO,sell_order_response_data)
        except Exception as e:
            addLogDetails(ERROR, "Error in selling previous order")
            addLogDetails(ERROR,str(e))

        buy_order_details = {VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: currentPremiumPlaced,
                             SYMBOL_TOKEN: BrokerObject.getTokenForSymbol(currentPremiumPlaced),
                             TRANSACTION_TYPE: BUY, ORDER_TYPE: MARKET, PRODUCT_TYPE: INTRADAY, DURATION: DAY,
                             QUANTITY: user_qty}
        addLogDetails(INFO,buy_order_details)
        order_response = BrokerObject.placeOrder(buy_order_details)




        order_response_data = order_response.get("data", {})
        data = {
            "current_premium": order_response_data.get("script"),
            "order_id": order_response_data.get("orderid"),
            "unique_order_id": order_response_data.get("uniqueorderid")
        }
        addLogDetails(INFO, f"Manual Order placed UserId ={user_email} LTP while placing order : {ltpDetails} data = {buy_order_details}")
        updateManualOrderDetails(user_email, index_name, data=data)
        order_response_from_broker = BrokerObject.getOrderDetails(order_response_data.get("uniqueorderid"))
        addLogDetails(INFO, "order_response_from_broker")
        addLogDetails(INFO,order_response_from_broker)
        #option_buy_price=order_response_from_broker["data"][""]
        addLogDetails(INFO,f"Manual Order placed UserId ={user_email} data = {order_response}")
        # exit_order_details = {VARIETY: NORMAL, EXCHANGE: NFO, TRADING_SYMBOL: currentPremiumPlaced,
        #                       SYMBOL_TOKEN: BrokerObject.getTokenForSymbol(currentPremiumPlaced),
        #                       TRANSACTION_TYPE: SELL, ORDER_TYPE: ORDER_TYPE_LIMIT, PRODUCT_TYPE: INTRADAY, DURATION: DAY,
        #                       QUANTITY: user_qty, PRICE: float(ltpDetails)+target}
        # addLogDetails(INFO, exit_order_details)
        # exit_order_response = BrokerObject.placeOrder(exit_order_details)
        # addLogDetails(INFO, exit_order_response)
        return JsonResponse({STATUS: SUCCESS, MESSAGE: str(order_response_from_broker), TASK_STATUS: True})

    except Exception as e:
        addLogDetails(ERROR,str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR, TASK_STATUS: False})