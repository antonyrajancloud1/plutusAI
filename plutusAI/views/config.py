"""Per-user settings: strategy configs, strategies, broker details, Telegram."""
from django.http import JsonResponse

from plutusAI.models import (
    BrokerDetails, Configuration, FlashDetails, ManualOrders, ScalperDetails,
    TelegramSettings,
)
from plutusAI.server.api import GET, POST, PUT, api, fail, ok
from plutusAI.server.base import (
    get_broker_details_using_id, get_broker_details_using_id_and_group,
    get_index_group_by_broker, remove_data_from_list, remove_spaces_from_json,
    validate_char_fields, validate_float_field, validate_levels,
    validate_numeric_fields,
)
from plutusAI.server.constants import (
    ALL_CONFIG_VALUES, AVAILABLE_BROKERS, BROKER_DETAILS_ADDED,
    BROKER_DETAILS_UPDATED, CONFIG_VALUES_UPDATED, FLASH_VALUES_UPDATED,
    INDEX_GROUP, INDEX_NAME, INDEX_NOT_FOUND, SCALPER_VALUES_UPDATED,
    TELEGRAM_CHAT_ID, TELEGRAM_NOTIFY_ON_ERROR,
)

# Never writable from the API: row identity and ownership.
LOCKED_FIELDS = {"id", "user_id"}


def _rows(model, email, **filters):
    """User's rows without id/user_id (the shape the frontend expects)."""
    return remove_data_from_list(list(model.objects.filter(user_id=email, **filters).values()))


def _editable(data, extra_locked=()):
    locked = LOCKED_FIELDS | set(extra_locked)
    return {k: v for k, v in data.items() if k not in locked}


# ------------------------------------------------- strategy configs (one per index)


def _config_getter(model, all_response):
    @api(GET)
    def view(request):
        if INDEX_NAME in request.GET:
            rows = _rows(model, request.email, index_name=request.GET[INDEX_NAME])
            return JsonResponse(rows[0]) if rows else fail(INDEX_NOT_FOUND)
        return all_response(_rows(model, request.email))

    return view


def _config_updater(model, message, check_levels=False, extra_locked=()):
    @api(PUT)
    def view(request):
        data = remove_spaces_from_json(request.json)
        validate_numeric_fields(data)
        validate_float_field(data)
        if check_levels:
            validate_levels(data)
        rows = model.objects.filter(user_id=request.email, index_name=data.get(INDEX_NAME))
        if not rows.exists():
            return fail(INDEX_NOT_FOUND)
        rows.update(**_editable(data, extra_locked))
        return ok(message, data=_rows(model, request.email, index_name=data.get(INDEX_NAME))[0])

    return view


def _all_configs(rows):
    return JsonResponse({ALL_CONFIG_VALUES: rows})


get_config_values = _config_getter(Configuration, _all_configs)
get_scalper_values = _config_getter(ScalperDetails, _all_configs)
get_flash_values = _config_getter(FlashDetails, lambda rows: ok(rows, task_status=True))

update_config_values = _config_updater(Configuration, CONFIG_VALUES_UPDATED, check_levels=True)
update_scalper_values = _config_updater(ScalperDetails, SCALPER_VALUES_UPDATED)
update_flash_values = _config_updater(FlashDetails, FLASH_VALUES_UPDATED)
update_manual_order_values = _config_updater(
    ManualOrders, CONFIG_VALUES_UPDATED, check_levels=True,
    extra_locked=("index_name", "strategy_name", "order_status"),
)


# ------------------------------------------------- webhook strategies (ManualOrders)


@api(GET)
def getAllManualOrderDetails(request):
    index = request.GET.get(INDEX_NAME)
    rows = ManualOrders.objects.filter(user_id=request.email)
    if index:
        rows = rows.filter(index_name=index)
    rows = list(rows.values())
    if rows:
        return ok(rows, task_status=True)
    return fail(INDEX_NOT_FOUND if index else "No orders found")


@api(GET)
def getStrategyDetails(request):
    rows = ManualOrders.objects.filter(user_id=request.email)
    if request.GET.get(INDEX_NAME):
        rows = rows.filter(index_name=request.GET[INDEX_NAME])
    return ok(data=list(rows.values()))


@api(POST, expose_errors=True)
def addStrategy(request):
    data = request.json
    name, index = data.get("strategy_name"), data.get("index_name")
    if not name or not index:
        return fail("strategy_name and index_name are mandatory")
    if ManualOrders.objects.filter(user_id=request.email, strategy_name=name).exists():
        return fail(f"Strategy '{name}' already exists")
    ManualOrders.objects.create(
        user_id=request.email,
        strategy_name=name,
        index_name=index,
        strike=data.get("strike"),
        lots=data.get("lots"),
        on_candle_close=data.get("on_candle_close", False),
        producttype=data.get("producttype", "INTRADAY"),
        timeframe=data.get("timeframe", "FIVE_MINUTE"),
        index_group=data.get("index_group", "indian_index"),
        strategy_type="custom",
    )
    return ok("Strategy added", strategy_name=name)


@api(PUT, expose_errors=True)
def updateStrategy(request):
    name, fields = request.json.get("strategy_name"), _editable(request.json.get("fields") or {})
    if not name or not fields:
        return fail("Invalid request")
    updated = ManualOrders.objects.filter(user_id=request.email, strategy_name=name).update(**fields)
    return ok("Updated successfully") if updated else fail("No record found")


@api(POST, expose_errors=True)
def deleteStrategy(request):
    name = request.json.get("strategy_name")
    if not name:
        return fail("Strategy name required")
    deleted, _ = ManualOrders.objects.filter(user_id=request.email, strategy_name=name).delete()
    return ok("Deleted successfully") if deleted else fail("No record found")


# ------------------------------------------------- broker details

BROKER_REQUIRED_FIELDS = [
    "user_id", "broker_name", "broker_user_id", "is_demo_trading_enabled",
    "broker_password", "broker_forex_server",
]


@api(GET)
def get_broker_details(request):
    if "broker_name" in request.GET:
        return get_broker_details_using_id_and_group(request.email, request.GET["broker_name"])
    return get_broker_details_using_id(request.email)


@api(POST)
def add_broker_details(request):
    data = request.json
    missing = [f for f in BROKER_REQUIRED_FIELDS if f not in data]
    if missing:
        return fail(f"Missing fields: {', '.join(missing)}")
    model_fields = {f.name for f in BrokerDetails._meta.fields}
    row = {k: v for k, v in data.items() if k in model_fields}
    row["index_group"] = get_index_group_by_broker(AVAILABLE_BROKERS, data["broker_name"])[0]
    row["token_status"] = "added"
    BrokerDetails.objects.create(**row)
    return ok(BROKER_DETAILS_ADDED)


@api(PUT)
def update_broker_details(request):
    data = request.json
    validate_char_fields(data)
    BrokerDetails.objects.filter(
        user_id=request.email, index_group=data.get(INDEX_GROUP)
    ).update(**_editable(data))
    return ok(BROKER_DETAILS_UPDATED)


# ------------------------------------------------- Telegram (per user)


def _telegram_body(settings):
    return {
        TELEGRAM_CHAT_ID: (settings.chat_id or "") if settings else "",
        TELEGRAM_NOTIFY_ON_ERROR: settings.notify_on_error if settings else False,
    }


@api(GET)
def get_telegram_settings(request):
    return ok(**_telegram_body(TelegramSettings.objects.filter(user_id=request.email).first()))


@api(POST)
def update_telegram_settings(request):
    settings, _ = TelegramSettings.objects.update_or_create(
        user_id=request.email,
        defaults={
            TELEGRAM_CHAT_ID: request.json.get(TELEGRAM_CHAT_ID, "").strip(),
            TELEGRAM_NOTIFY_ON_ERROR: request.json.get(TELEGRAM_NOTIFY_ON_ERROR, False),
        },
    )
    return ok("Telegram settings updated", **_telegram_body(settings))
