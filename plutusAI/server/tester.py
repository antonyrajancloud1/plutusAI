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

    candle_data_df = BrokerObject.getCandleData(NFO, 35075, "2024-09-06 10:37", "2024-09-06 10:38", "ONE_MINUTE")
    print(candle_data_df)
    return JsonResponse({STATUS: SUCCESS, MESSAGE: getBrokerageForLots(1,15)})
