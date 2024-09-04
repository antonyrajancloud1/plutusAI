from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from django.http import JsonResponse

from plutusAI.models import BrokerDetails
from plutusAI.server.base import getBrokerageForLots
from plutusAI.server.broker.AngelOneBroker import AngelOneBroker
from plutusAI.server.broker.Broker import Broker
from plutusAI.server.constants import *
from plutusAI.server.supportResistance.AngelOneSR import SupportResistanceCalculator
import requests

def testerCheck(request):
    user_email="antonyrajan.d@gmail.com"
    BrokerObject = Broker(user_email, INDIAN_INDEX).BrokerObject
    user_broker_data = BrokerDetails.objects.filter(user_id=ADMIN_USER_ID, index_group=INDIAN_INDEX)
    BrokerObject = AngelOneBroker(user_broker_data)

    # Initialize WebSocket parameters
    correlation_id = "admin_ws"
    symbol_token = BrokerObject.getTokenForSymbol(BANKNIFTY_FUTURES)
    tokens = [symbol_token]  # Define your tokens
    global ltp_values_dict
    global start_time_dict
    ltp_values_dict = {}
    start_time_dict = {}


    def createWebSocketObj(token, exchangeType):
        global mode
        global token_list
        action = 1
        mode = 2

        token_list = [
            {
                "exchangeType": exchangeType,
                "tokens": token
            }
        ]
        swsObj = SmartWebSocketV2(BrokerObject.auth_token, BrokerObject.broker_api_token, BrokerObject.broker_user_id,
                                  BrokerObject.feed_token, max_retry_attempt=2)
        return swsObj

    sws = None

    def on_open(wsapp):
        global token_list
        print("Opennn")
        # sws.subscribe(correlation_id, 1, [{"exchangeType": 2, "tokens": tokens}])
        sws.subscribe(correlation_id, 2, token_list)

    def on_data(wsapp, message):
        data = {"token":message["token"],"exchange_timestamp":message ["exchange_timestamp"],"ltp":message["last_traded_price"]/100,"closed_price":message["closed_price"]}
        print(data)

    def on_error(wsapp, error):
        print(str(error))

    def on_close(wsapp):
        print( "WebSocket connection closed")

    def close_connection():
        sws.close_connection()
        # addLogDetails(INFO, "WebSocket connection closed manually")

    sws = createWebSocketObj(tokens, 2)
    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error
    sws.on_close = on_close

    sws.connect()

    def on_error(wsapp, error):
        # Handle WebSocket errors
        # addLogDetails(ERROR, str(error))
        print("WebSocket connection error")

    def on_close(wsapp):
        # Handle WebSocket closing
        # addLogDetails(INFO, "WebSocket connection closed")
        print("WebSocket connection on_close")

    def close_connection():
        # Close WebSocket connection
        sws.close_connection()
        # addLogDetails(INFO, "WebSocket connection closed manually")

    # Create and configure the WebSocket
    sws = createWebSocketObj([35165], 2)
    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error
    sws.on_close = on_close

    # Connect to the WebSocket
    sws.connect()

    return JsonResponse({STATUS: SUCCESS, MESSAGE: getBrokerageForLots(1,15)})
