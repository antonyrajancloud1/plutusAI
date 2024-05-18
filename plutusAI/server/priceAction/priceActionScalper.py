# myapp/tasks.py
import json
from celery.result import AsyncResult
from celery import shared_task
import time
from celery import current_task
import pandas as pd
import requests
from plutusAI.models import *
from plutusAI.server.base import *
from plutusAI.server.priceAction.NSEPriceAction import NSEPriceAction
from plutus import celery
from plutus.celery import app


@shared_task
def start_index_job(user_email, index):
    task_id = current_task.request.id
    JobDetails.objects.create(
        user_id=user_email,
        index_name=index,
        job_id=task_id,
    )
    index_data = IndexDetails.objects.filter(index_name=index)
    index_group_name = get_index_group_name(index_data)
    if index_group_name == INDIAN_INDEX:
        NSEPriceAction(user_email, index, INDIAN_INDEX)
    elif index_group_name == FOREX_INDEX:
        addLogDetails(INFO, "Forex market")


@shared_task
def terminate_task(user_email, index):
    try:
        user_data = JobDetails.objects.filter(user_id=user_email, index_name=index)
        job_details = list(user_data.values())
        if len(job_details) > 0:
            task_id = job_details[0]['job_id']
            result = AsyncResult(str(task_id))
            result.revoke(terminate=True)
            if user_data.exists():
                user_data.delete()
                updateIndexConfiguration(user_email, index, data=STAGE_STOPPED)

                return JsonResponse({STATUS: SUCCESS, MESSAGE: "Index Stopped"})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: "Index not running"})

    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})
