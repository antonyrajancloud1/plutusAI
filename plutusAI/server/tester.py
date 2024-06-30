from datetime import datetime
from celery.result import AsyncResult
import time
from django.http import JsonResponse
from plutusAI.models import BrokerDetails
from plutusAI.server.base import addLogDetails, getTokenUsingSymbol, getTradingSymbol, current_time
from plutusAI.server.broker.AngelOneBroker import AngelOneBroker
from plutusAI.server.constants import *

def testerCheck(request):
    # raw_text = request.body.decode('utf-8')
    # result = AsyncResult(raw_text)
    started_time = current_time()
    time_string = started_time.split(" ")[1]
    now = datetime.strptime(time_string, "%H:%M:%S").time()
    target_time = datetime.strptime("09:15:00", "%H:%M:%S").time()
    print(now)
    print(target_time)
    if now < target_time:
        print("The current time is less than 09:15 AM.")
    else:
        print("The current time is 09:15 AM or later.")
    print("result")
    return JsonResponse({STATUS: SUCCESS, MESSAGE: str("result.state")})