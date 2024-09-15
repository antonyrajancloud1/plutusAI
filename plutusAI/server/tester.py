from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from django.http import JsonResponse

from plutusAI.models import BrokerDetails
from plutusAI.server.base import getBrokerageForLots, getTradingSymbol
from plutusAI.server.broker.AngelOneBroker import AngelOneBroker
from plutusAI.server.broker.Broker import Broker
from plutusAI.server.constants import *
from plutusAI.server.supportResistance.AngelOneSR import SupportResistanceCalculator
import requests

def testerCheck(request):
    user_email="antonyrajan.d@gmail.com"
    index_name = "bank_nifty"
    strike=200
    user_qty=15
    BrokerObject = Broker(user_email, INDIAN_INDEX).BrokerObject
    user_broker_data = BrokerDetails.objects.filter(user_id=ADMIN_USER_ID, index_group=INDIAN_INDEX)
    BrokerObject = AngelOneBroker(user_broker_data)

    currentPremiumPlaced = f"{getTradingSymbol(index_name)}{BrokerObject.getCurrentAtm(index_name) - int(strike)}CE"

    # Define the buy order details
    buy_order_details = {
        VARIETY: NORMAL,
        EXCHANGE: NFO,
        TRADING_SYMBOL: currentPremiumPlaced,
        SYMBOL_TOKEN: BrokerObject.getTokenForSymbol(currentPremiumPlaced),
        TRANSACTION_TYPE: BUY,
        ORDER_TYPE: MARKET,
        PRODUCT_TYPE: INTRADAY,
        DURATION: DAY,
        QUANTITY: user_qty
    }
    order_response = BrokerObject.placeOrder(buy_order_details)
    optionDetails = BrokerObject.getCurrentPremiumDetails(NFO, currentPremiumPlaced)
    print(optionDetails)
    print(buy_order_details)
    return JsonResponse({STATUS: SUCCESS, MESSAGE: order_response})
