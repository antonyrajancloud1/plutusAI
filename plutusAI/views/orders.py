"""Order endpoints: manual buttons, TradingView webhooks (?token=), order book, forex."""
import json

from django.http import JsonResponse

from plutusAI.models import LogDetails, ManualOrders, OrderBook
from plutusAI.server.api import ADMIN_TOKEN, GET, POST, SESSION, TOKEN, api, ok
from plutusAI.server.base import (
    getCurrentTimestamp, getOpenOrdersUsingEmail, getStrategySummaryUsingEmail,
    remove_spaces_from_json,
)
from plutusAI.server.broker.Broker import Broker
from plutusAI.server.constants import (
    BUY, EXIT_PRICE, EXIT_TIME, FAILED, FOREX_INDEX, ID, INDEX_NAME, INDIAN_INDEX,
    ORDER_BOOK_DETAILS, SELL, STATUS, STRATEGY, TASK_STATUS,
)
from plutusAI.server.manualOrder import (
    exitOrderWebhook, submit_exitOrderWebhook, submit_modifyToMarketOrder,
    submit_triggerOrder, triggerOrder,
)

ENTRY_ALERT = ("ENTRY SIGNAL FAILED - NO POSITION TAKEN",
               "No order was sent. Take the entry manually in AngelOne if needed.")
EXIT_ALERT = ("EXIT SIGNAL FAILED - POSITION MAY STILL BE OPEN",
              "Open AngelOne and exit the position manually NOW.")


def _strategy_settings(email, index):
    row = ManualOrders.objects.filter(user_id=email, index_name=index).values().first()
    if not index or not row:
        raise Exception(f"No strategy settings found for index '{index}'")
    return remove_spaces_from_json(row)


def _strategy(data):
    return data.get(STRATEGY, "DefaultStrategy")


def _log_signal(request, kind):
    LogDetails.objects.create(
        user_id=request.email,
        index_name=request.json[INDEX_NAME],
        log=f"{kind} Order triggered for strategy {_strategy(request.json)}",
        time=getCurrentTimestamp(),
    )


def _failed(response):
    """The flow's own failure response (it has already logged and alerted), else None."""
    return response if json.loads(response.content).get(STATUS) == FAILED else None


def _entry_view(side, run_now, message, auth, log_kind=None):
    """Entry signal: sync for the UI buttons (result is returned), queued for webhooks."""

    @api(POST, auth=auth, alert=ENTRY_ALERT)
    def view(request):
        if log_kind:
            _log_signal(request, log_kind)
        settings = _strategy_settings(request.email, request.json[INDEX_NAME])
        if not run_now:
            submit_triggerOrder(request.email, settings, request.json, side)
            return ok(message)
        return _failed(triggerOrder(request.email, settings, request.json, side)) or ok(message)

    return view


placeBuyOrderManual = _entry_view(BUY, True, "Message Exists BUY", SESSION)
placeSellOrderManual = _entry_view(SELL, True, "Message Exists SELL", SESSION)
placeBuyOrderWebHook = _entry_view(BUY, False, "Message Done", TOKEN, "Buy")
placeSellOrderWebHook = _entry_view(SELL, False, "Message Done", TOKEN, "Sell")


@api(POST, alert=EXIT_ALERT)
def placeExitOrderManual(request):
    return _failed(exitOrderWebhook(_strategy(request.json), request.json, request.email)) or ok("Message Done")


@api(POST, auth=TOKEN, alert=EXIT_ALERT)
def placeExitOrderWebHook(request):
    _log_signal(request, "Exit")
    submit_exitOrderWebhook(_strategy(request.json), request.json, request.email)
    return ok("Message Exists SELL")


@api(POST, auth=TOKEN, alert=ENTRY_ALERT)
def modifyToMarketOrderWebHook(request):
    settings = _strategy_settings(request.email, request.json[INDEX_NAME])
    submit_modifyToMarketOrder(request.email, settings, _strategy(request.json), BUY)
    return ok("Modified")


@api(POST, auth=ADMIN_TOKEN, alert=EXIT_ALERT)
def exitAllOrdersWebHook(request):
    open_orders = OrderBook.objects.filter(exit_price=None)
    if not open_orders.exists():
        return ok("No open orders to exit")
    for order in open_orders:
        exitOrderWebhook(
            order.strategy, {INDEX_NAME: order.index_name, STRATEGY: order.strategy}, order.user_id
        )
    return ok("done for the day")


# ------------------------------------------------- read-only order data


@api(GET)
def get_order_book_details(request):
    rows = list(OrderBook.objects.filter(user_id=request.email).order_by("-entry_time").values())
    for row in rows:
        row.pop(ID)
        row[EXIT_PRICE] = row[EXIT_PRICE] or ""
        row[EXIT_TIME] = row[EXIT_TIME] or ""
    return JsonResponse({ORDER_BOOK_DETAILS: rows})


@api(GET)
def getOpenOrders(request):
    return getOpenOrdersUsingEmail(request.email, Broker(request.email, INDIAN_INDEX).BrokerObject)


@api(GET)
def getStrategySummary(request):
    return ok(summary=getStrategySummaryUsingEmail(request.email), **{TASK_STATUS: True})


# ------------------------------------------------- forex (Exness) webhooks


def _forex_view(action, message=None):
    @api(POST, auth=TOKEN)
    def view(request):
        broker = Broker(request.email, FOREX_INDEX).BrokerObject
        response = action(broker, request.json)
        return ok(message or response)

    return view


placeForexBuy = _forex_view(lambda broker, data: broker.placeOrderForex(0, data), "Buy Completed")
placeForexSell = _forex_view(lambda broker, data: broker.placeOrderForex(1, data))
closeForexSell = _forex_view(lambda broker, data: broker.exitOrderForex(data))
