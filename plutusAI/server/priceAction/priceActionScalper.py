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
from plutusAI.server.broker.Broker import Broker
from plutusAI.server.priceAction.FlashTrade import  IndexPriceActionChecker
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
    print("start flash job")
    task_id = current_task.request.id
    print(task_id)
    JobDetails.objects.create(
        user_id=user_email,
        index_name=index,
        job_id=task_id,
        strategy=STRATEGY_FLASH
    )
    try:
        flash_settings = FlashDetails.objects.filter(user_id=user_email, index_name=index).first()
        if not flash_settings:
            addLogDetails(ERROR, f"[start_flash_job] Flash settings not found for {user_email}/{index}")
            return

        # A Stop click can arrive while this task is still queued.  In that
        # case, do not turn the requested stop back into a running strategy.
        if flash_settings.status not in {STAGE_INITIATED["status"], STAGE_RUNNING["status"]}:
            addLogDetails(INFO, f"[start_flash_job] Flash start cancelled for {user_email}/{index}")
            return

        index_data = IndexDetails.objects.filter(index_name=index)
        index_group_name = get_index_group_name(index_data)
        if index_group_name != INDIAN_INDEX:
            addLogDetails(INFO, f"[start_flash_job] Flash is not supported for {index_group_name}")
            return

        index_details = index_data.values().first() or {}
        lot_size = int(index_details.get(QTY) or 1)
        lots = max(1, int(flash_settings.lots or 1))
        user_qty = lot_size * lots
        max_loss_points = float(flash_settings.max_loss or 0) / user_qty
        if max_loss_points <= 0:
            max_loss_points = 10.0
        trailing_points = float(flash_settings.trailing_points or 10)
        profit_protection_start = float(flash_settings.average_points or trailing_points)

        def flash_is_running():
            return FlashDetails.objects.filter(
                user_id=user_email,
                index_name=index,
                status=STAGE_RUNNING["status"],
            ).exists()

        config_dict = {
            "levels": "",
            "strike": flash_settings.strike,
            "trend_check_points": flash_settings.trend_check_points,
            "user_qty": user_qty,
            "is_place_sl_required": True,
            "initialSL": max_loss_points,
            "hard_stop_loss_points": max_loss_points,
            "trailing_points": trailing_points,
            "profit_protection_start": profit_protection_start,
            "profit_lock_points": 0,
            "_should_continue": flash_is_running,
        }

        updateFlashConfiguration(user_email, index, STAGE_RUNNING)
        broker_obj = Broker(user_email, index_group_name).BrokerObject
        checker = IndexPriceActionChecker(
            index_name=index,
            user_email=user_email,
            BrokerObject=broker_obj,
            config=config_dict,
        )
        checker.evaluatePriceAction()
    except Exception as e:
        addLogDetails(ERROR, f"[start_flash_job] {user_email}/{index}: {e}")
    finally:
        JobDetails.objects.filter(job_id=task_id).delete()
        updateFlashConfiguration(user_email, index, STAGE_STOPPED)
