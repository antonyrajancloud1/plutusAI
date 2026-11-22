"""Background jobs, Celery control, users/plans, API tokens, index data, logs."""
import subprocess
import time
from datetime import datetime, timedelta

from celery.result import AsyncResult
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

from plutusAI.models import (
    IndexDetails, JobDetails, LogDetails, PaymentDetails, TelegramBotConfig,
)
from plutusAI.server.api import ADMIN, ADMIN_TOKEN, GET, POST, PUT, api, fail, ok
from plutusAI.server.base import (
    addLogDetails, add_user_and_populate_data, admin_check, remove_data_from_list, start_ws_job,
    terminate_task, updateExpiryDetails, updateFlashConfiguration,
    updateIndexConfiguration, updateScalperDetails,
)
from plutusAI.server.broker.AngelOne.AngelOneAuth import AngelOneAuth
from plutusAI.server.broker.Broker import Broker
from plutusAI.server.constants import (
    ADMIN_USER_ID, ERROR, HTTP_JOB, INDEX_NAME, INDIAN_INDEX, INFO, MESSAGE, PLAN_DETAILS,
    SCALPER, SOCKET_JOB, STAGE_INITIATED, STRATEGY, STRATEGY_FLASH, STRATEGY_HUNTER,
    TOKEN_GENERATED,
)
from plutusAI.server.priceAction.priceActionScalper import (
    start_flash_job, start_index_job, start_scalper_task,
)

# ------------------------------------------------- strategy jobs


def _display(index_name):
    return index_name.replace("_", " ").title().replace(" ", "")


def _start_job(strategy, update_stage, task, label, running, started):
    @api(POST)
    def view(request):
        index = request.json.get(INDEX_NAME)
        name = _display(index)
        addLogDetails(INFO, f"{label} started for user: {request.email} for index :{name}")
        if JobDetails.objects.filter(user_id=request.email, index_name=index, strategy=strategy).exists():
            return fail(f"{name} {running}")
        update_stage(request.email, index, data=STAGE_INITIATED)
        task.delay(request.email, index)
        return ok(f"{name} {started}")

    return view


start_index = _start_job(STRATEGY_HUNTER, updateIndexConfiguration, start_index_job,
                         "Hunter", "process running", "started")
start_scalper = _start_job(SCALPER, updateScalperDetails, start_scalper_task,
                           "scalper", "scalper running", "scalper started")
start_flash = _start_job(STRATEGY_FLASH, updateFlashConfiguration, start_flash_job,
                         "Flash", "Flash running", "flash started")


@api(POST)
def stop_index(request):
    return terminate_task(request.email, request.json.get(INDEX_NAME), request.json.get(STRATEGY))


# ------------------------------------------------- market data websocket jobs

WS_JOBS = {"1": SOCKET_JOB, "2": HTTP_JOB, "3": HTTP_JOB}


@api(POST, auth=ADMIN)
def start_ws(request):
    ws_type = str(request.json.get("ws_type"))
    if ws_type not in WS_JOBS:
        return fail("Invalid ws_type", task_status=False)
    job = WS_JOBS[ws_type]
    if JobDetails.objects.filter(user_id=ADMIN_USER_ID, index_name=job, strategy=job).exists():
        return fail("Socket running", task_status=True)
    return start_ws_job(ws_type)


@api(POST, auth=ADMIN)
def stop_ws(request):
    ws_type = str(request.json.get("ws_type"))
    if ws_type not in WS_JOBS:
        return fail("Invalid ws_type", task_status=False)
    return terminate_task(ADMIN_USER_ID, WS_JOBS[ws_type], WS_JOBS[ws_type])


@api(GET)
def check_task_status(request):
    job = JobDetails.objects.filter(
        user_id=ADMIN_USER_ID, index_name=SOCKET_JOB, strategy=SOCKET_JOB
    ).values().first()
    if not job:
        return ok("No Socket Job Present", task_status=False)
    if str(AsyncResult(job["job_id"]).status) == "PENDING":
        return ok("Socket running", task_status=True)
    return fail("Socket not running", task_status=False)


# ------------------------------------------------- Celery worker

CELERY_APP = "plutus.celery"
CELERY_START = f"celery -A {CELERY_APP} worker --loglevel=info --autoscale=100,3"


def is_celery_running():
    ps = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return any("celery" in line and CELERY_APP in line for line in ps.stdout.splitlines())


def stopCelery():
    if not is_celery_running():
        return {"success": False, "message": "Celery is not running.", "task_status": False}
    try:
        subprocess.run(["pkill", "-f", f"celery -A {CELERY_APP}"], check=True)
        return {"success": True, "message": "Celery stopped successfully.", "task_status": True}
    except subprocess.CalledProcessError as e:
        return {"success": False, "message": f"Failed to stop Celery: {e}"}


@api(GET)
def check_celery_status(request):
    running = is_celery_running()
    return JsonResponse({"celery_running": running, "details": f"Celery is {'' if running else 'NOT '}running."})


@api(POST, auth=ADMIN)
def stop_celery(request):
    return JsonResponse(stopCelery())


@api(POST, auth=ADMIN)
def restart_celery(request):
    if is_celery_running():
        if not stopCelery()["success"]:
            return JsonResponse({"success": False, "message": "Failed to stop Celery. Restart aborted."})
        time.sleep(2)
    subprocess.Popen(CELERY_START, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return JsonResponse({"success": True, "message": "Celery restarted successfully.", "task_status": True})


# ------------------------------------------------- users, plans, API tokens


@api(POST, auth=ADMIN)
def add_user(request):
    return add_user_and_populate_data(request.json)


@api(GET)
def get_plan_details(request):
    rows = list(PaymentDetails.objects.filter(user_id=request.email).values())
    return JsonResponse({PLAN_DETAILS: remove_data_from_list(rows)})


@api(PUT, auth=ADMIN)
def edit_plan_details(request):
    data = request.json
    now = datetime.now()
    data["renew_date"] = (now + timedelta(days=int(data.get("renew_date")))).strftime("%Y-%m-%d %H:%M:%S")
    plans = PaymentDetails.objects.filter(user_id=data.get("user_id"))
    if plans.exists():
        plans.update(**data)
    else:
        PaymentDetails.objects.create(
            user_id=data.get("user_id"),
            registed_date=now.strftime("%Y-%m-%d %H:%M:%S"),
            renew_date=data["renew_date"],
            opted_index=data.get("opted_index"),
        )
    return ok(data)


@api(POST)
def getAuthToken(request):
    token, _ = Token.objects.get_or_create(user=request.user)
    return ok(token.key)


@api(POST)
def regenerateAuthToken(request):
    Token.objects.filter(user=request.user).delete()
    return ok(Token.objects.create(user=request.user).key)


@api(GET)
def check_admin(request):
    return ok(is_admin=admin_check(request.user))


# ------------------------------------------------- broker session


@api(POST)
def reGenerateAccessToken(request):
    AngelOneAuth(request.email)
    return ok(TOKEN_GENERATED, task_status=True)


@api(GET)
def checkBrokerTokenStatus(request):
    try:
        profile = Broker(request.email, INDIAN_INDEX).BrokerObject.checkProfile()
    except Exception as e:
        addLogDetails(ERROR, f"{request.email} :: checkBrokerTokenStatus error: {e}")
        return fail("token_is_invalid", task_status=False)
    if profile[MESSAGE] == "SUCCESS":
        return ok("token_is_valid", task_status=True)
    return fail(profile["errorcode"], task_status=False)


# ------------------------------------------------- index data


@api(GET)
def getIndexDetails(request):
    rows = IndexDetails.objects.values("index_name", "index_token", "ltp", "qty", "current_expiry", "next_expiry")
    return ok({"index_data": list(rows)})


@api(POST, auth=ADMIN_TOKEN)
def updateIndexExpiryDetails(request):
    updateExpiryDetails()
    return ok("Expiry details Updated", task_status=True)


# ------------------------------------------------- Telegram bot (admin only: holds bot tokens)

BOT_FIELDS = ("bot_id", "admin_bot_id", "admin_chat_ids")


def _bot_body(config):
    return {f: (getattr(config, f) or "") if config else "" for f in BOT_FIELDS}


@api(GET, auth=ADMIN)
def get_telegram_bot_config(request):
    return ok(**_bot_body(TelegramBotConfig.objects.first()))


@api(POST, auth=ADMIN)
def update_telegram_bot_config(request):
    config = TelegramBotConfig.objects.first() or TelegramBotConfig()
    for field in BOT_FIELDS:
        setattr(config, field, request.json.get(field, "").strip())
    config.save()
    return ok("Bot configuration updated", **_bot_body(config))


# ------------------------------------------------- activity log


def _timestamp(value, end_of_day=False):
    """'YYYY-MM-DD' (or a raw epoch) -> epoch seconds; None if unparseable."""
    try:
        day = datetime.strptime(value, "%Y-%m-%d")
        return (day.replace(hour=23, minute=59, second=59) if end_of_day else day).timestamp()
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            return None


@api(GET, POST)
def getLogDetails(request):
    data = request.json or request.GET
    logs = LogDetails.objects.filter(user_id=request.email)
    if data.get(INDEX_NAME):
        logs = logs.filter(index_name=data[INDEX_NAME])
    logs = list(logs.values())

    if data.get("start_date") or data.get("end_date"):
        start = _timestamp(data.get("start_date")) if data.get("start_date") else None
        end = _timestamp(data.get("end_date"), end_of_day=True) if data.get("end_date") else None

        def in_range(log):
            ts = _timestamp(log.get("time"))
            return ts is not None and (start is None or ts >= start) and (end is None or ts <= end)

        logs = [log for log in logs if in_range(log)]
    return ok(data=logs)
