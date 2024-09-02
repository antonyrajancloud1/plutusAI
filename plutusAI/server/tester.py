from django.http import JsonResponse

from plutusAI.server.base import getBrokerageForLots
from plutusAI.server.broker.Broker import Broker
from plutusAI.server.constants import *
from plutusAI.server.supportResistance.AngelOneSR import SupportResistanceCalculator
import requests

def testerCheck(request):
    user_email="antonyrajan.d@gmail.com"
    BrokerObject = Broker(user_email, INDIAN_INDEX).BrokerObject
    opt_symb=BrokerObject.getTokenForSymbol("BANKNIFTY04SEP2451300CE")
    mod = {'orderid': '240902101267595', 'variety': 'NORMAL', 'exchange': 'NFO', 'tradingsymbol': "BANKNIFTY04SEP2451300CE","symboltoken": opt_symb,'transactiontype': 'BUY', 'ordertype': 'MARKET', 'producttype': 'INTRADAY', 'duration': 'DAY', 'quantity': 15}
    print(mod)
    data1=BrokerObject.modifyOrder(mod)
    print(data1)

    return JsonResponse({STATUS: SUCCESS, MESSAGE: getBrokerageForLots(1,15)})
