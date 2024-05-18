from datetime import datetime
from celery.result import AsyncResult
import time
from django.http import JsonResponse
from plutusAI.models import BrokerDetails
from plutusAI.server.base import addLogDetails, getTokenUsingSymbol, getTradingSymbol
from plutusAI.server.broker.AngelOneBroker import AngelOneBroker
from plutusAI.server.constants import *

def testerCheck(request):
    raw_text = request.body.decode('utf-8')
    result = AsyncResult(raw_text)
    print(result)
    return JsonResponse({STATUS: SUCCESS, MESSAGE: str(result.state)})