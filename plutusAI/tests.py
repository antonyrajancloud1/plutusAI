from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .server.broker.AngelOneBroker import AngelOneBroker
from .server.manualOrder import *
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
import time

from .server.priceAction.hft import HighFrequencyTrading


@require_http_methods(["GET"])
def tester(request):

    user_email = "antonyrajan.d@gmail.com"

    index_data = IndexDetails.objects.filter(index_name="nifty")
    index_group_name = get_index_group_name(index_data)
    if index_group_name == INDIAN_INDEX:
        # FlashTrade(user_email, index, INDIAN_INDEX)
        broker_obj = Broker(user_email, index_group_name).BrokerObject
        broker_obj.getCurrentAtm("nifty")
        user_data = Configuration.objects.filter(user_id=user_email, index_name="nifty")
        config_dict = list(user_data.values())[0]
        print("values Generated")
        print(config_dict)
        checker = HighFrequencyTrading(index_name="nifty", user_email=user_email, BrokerObject=broker_obj)
        #checker.startHFT()
    return JsonResponse({"started":"abc"}, safe=False)
