from datetime import datetime
from celery.result import AsyncResult
import time
from django.http import JsonResponse
from plutusAI.models import BrokerDetails
from plutusAI.server.base import addLogDetails, getTokenUsingSymbol, getTradingSymbol, current_time
from plutusAI.server.broker.AngelOneBroker import AngelOneBroker
from plutusAI.server.constants import *
def check_task_status(task_id):
    result = AsyncResult(task_id)
    status_str = str(result.status)
    if status_str == 'PENDING':
        return True;
    else:
        return False;

def testerCheck(request):
    # raw_text = request.body.decode('utf-8')
    # result = AsyncResult(raw_text)
    task_id="802dee4d-1e8d-4478-858d-8616b8a2950f"
    status = check_task_status(task_id)
    print(f"Task {task_id} status: {status}")

    return JsonResponse({STATUS: SUCCESS, MESSAGE: str("result.state")})