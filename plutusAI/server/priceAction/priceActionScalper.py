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
from plutusAI.server.priceAction.FlashTrade import FlashTrade
from plutusAI.server.priceAction.NSEPriceAction import NSEPriceAction
from plutus import celery
from plutus.celery import app
from plutusAI.server.priceAction.Scalper import Scalper


@shared_task
def start_index_job(user_email, index):
    task_id = current_task.request.id
    JobDetails.objects.create(
        user_id=user_email,
        index_name=index,
        job_id=task_id,
        strategy=STRATEGY_HUNTER
    )
    index_data = IndexDetails.objects.filter(index_name=index)
    index_group_name = get_index_group_name(index_data)
    if index_group_name == INDIAN_INDEX:
        NSEPriceAction(user_email, index, INDIAN_INDEX)
    elif index_group_name == FOREX_INDEX:
        addLogDetails(INFO, "Forex market")



@shared_task
def start_scalper_task(user_email, index):
    task_id = current_task.request.id
    JobDetails.objects.create(
        user_id=user_email,
        index_name=index,
        job_id=task_id,
        strategy=SCALPER,
    )
    index_data = IndexDetails.objects.filter(index_name=index)
    index_group_name = get_index_group_name(index_data)
    if index_group_name == INDIAN_INDEX:
        Scalper(user_email, index, INDIAN_INDEX)
    elif index_group_name == FOREX_INDEX:
        addLogDetails(INFO, "Forex market")

@shared_task
def start_flash_job(user_email, index):
    task_id = current_task.request.id
    JobDetails.objects.create(
        user_id=user_email,
        index_name=index,
        job_id=task_id,
        strategy=STRATEGY_FLASH
    )
    index_data = IndexDetails.objects.filter(index_name=index)
    index_group_name = get_index_group_name(index_data)
    if index_group_name == INDIAN_INDEX:
        FlashTrade(user_email, index, INDIAN_INDEX)
    elif index_group_name == FOREX_INDEX:
        addLogDetails(INFO, "Forex market")
