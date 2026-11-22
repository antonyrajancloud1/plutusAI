"""Webhook / manual option orders.

triggerOrder         BUY signal -> CE entry, SELL signal -> PE entry (an opposite
                     open position is exited first).
exitOrderWebhook     exits the strategy's open position.
modifyToMarketOrder  converts a pending (stop-limit) entry into a market entry.

Every failure is logged and sent to Telegram with the trade details and what to do.
"""
from collections import defaultdict
from threading import RLock

from plutusAI.server.base import *
from plutusAI.server.broker.Broker import Broker
from plutusAI.server.constants import *

try:
    from plutusAI.server.telegram_notifier import sendMessageInTelegram, sendTradeAlert
except ModuleNotFoundError:

    def sendMessageInTelegram(message, user_email=None):
        pass

    def sendTradeAlert(title, user_email, error_msg, details=None, action=None):
        pass


PENDING_STATUSES = ("open", "trigger pending")
TIMEFRAME_TO_MINUTES = {
    "ONE_MINUTE": 1,
    "THREE_MINUTE": 3,
    "FIVE_MINUTE": 5,
    "TEN_MINUTE": 10,
    "FIFTEEN_MINUTE": 15,
    "THIRTY_MINUTE": 30,
    "ONE_HOUR": 60,
    "ONE_DAY": 1440,
}

executor = ThreadPoolExecutor(max_workers=150)
# One lock per user+strategy so duplicate signals can't open two positions.
# Re-entrant because triggerOrder calls exitOrderWebhook for reversals.
_strategy_locks = defaultdict(RLock)


def submit_triggerOrder(user_email, user_index_data, signal_data, order_type):
    executor.submit(triggerOrder, user_email, user_index_data, signal_data, order_type)


def submit_exitOrderWebhook(strategy, data, user_email):
    executor.submit(exitOrderWebhook, strategy, data, user_email)


def submit_modifyToMarketOrder(user_email, user_index_data, strategy, order_type):
    executor.submit(
        modifyToMarketOrder, user_email, user_index_data, strategy, order_type
    )


# ---------------------------------------------------------------- helpers


def _response(ok, message):
    return JsonResponse(
        {STATUS: SUCCESS if ok else FAILED, MESSAGE: message, TASK_STATUS: ok}
    )


def _exchange(index_name):
    return BFO if index_name == "sensex" else NFO


def _openPosition(user_email, strategy):
    return OrderBook.objects.filter(
        user_id=user_email, strategy=strategy, exit_price=None
    )


def _webhookDetails(user_email, index_name, strategy):
    return WebhookDetails.objects.filter(
        user_id=user_email, index_name=index_name, strategy=strategy
    ).values().first()


def _productType(user_email, index_name):
    return (
        ManualOrders.objects.filter(user_id=user_email, index_name=index_name)
        .values()
        .first()[PRODUCT_TYPE]
    )


def _number(value):
    try:
        number = float(value)
        return number if number > 0 else None
    except (TypeError, ValueError):
        return None


def _cancelPending(broker, webhook, status):
    # Stop-limit entries ("trigger pending") must be cancelled with their own variety.
    variety = STOPLOSS if status == "trigger pending" else NORMAL
    broker.cancelOrder(webhook.get(ORDER_ID), variety)


def _pnl(exit_price, entry_price, qty):
    return str((float(exit_price) - float(entry_price)) * int(qty))


def buildOrder(broker, symbol, side, qty, product_type, exchange, trigger=None):
    """Market order, or a stop-limit order at `trigger` when one is given."""
    order = {
        VARIETY: NORMAL,
        EXCHANGE: exchange,
        TRADING_SYMBOL: symbol,
        SYMBOL_TOKEN: broker.getTokenForSymbol(symbol),
        TRANSACTION_TYPE: side,
        ORDER_TYPE: MARKET,
        PRODUCT_TYPE: product_type,
        DURATION: DAY,
        QUANTITY: qty,
    }
    if trigger is not None:
        order.update(
            {VARIETY: STOPLOSS, ORDER_TYPE: ORDER_TYPE_SL, TRIGGER_PRICE: trigger, PRICE: trigger}
        )
    return order


def ensureOrderAccepted(response, trading_symbol):
    # placeOrderFullResponse returns status=False (not an exception) on rejection.
    if not response or not response.get("status"):
        response = response or {}
        raise Exception(
            f"Broker rejected order for {trading_symbol}: "
            f"{response.get('message', 'no response')} ({response.get('errorcode', '')})"
        )


def placeAndVerify(broker, order, user_email):
    """Places the order; returns (order_id, unique_order_id) or raises on rejection."""
    response = broker.placeOrder(order)
    addLogDetails(INFO, f"{user_email} :: Order response: {response}")
    ensureOrderAccepted(response, order[TRADING_SYMBOL])
    data = response.get("data") or {}
    return data.get("orderid"), data.get("uniqueorderid")


def fillPrice(broker, unique_order_id, *fallbacks):
    """Best known fill price: broker fill details first, then the given fallbacks."""
    details = broker.getOrderDetails(unique_order_id) or {}
    for value in (details.get("averageprice"), details.get(PRICE), *fallbacks):
        if _number(value):
            return value
    return None


def entryTrigger(broker, symbol, ltp, exchange, timeframe):
    """On-candle-close entries wait above the last candle high; None means market."""
    minutes = TIMEFRAME_TO_MINUTES.get(timeframe, 6)
    from_time = str(get_previous_n_minute_start(get_current_minute_start(), False, minutes + 1))
    to_time = str(get_next_minute_start_ms(get_current_minute_start(), False))
    token = broker.getTokenForSymbol(symbol)
    try:
        candles = broker.getCandleData(exchange, token, from_time, to_time, timeframe)
        if candles is None or candles.empty or HIGH not in candles.columns:
            addLogDetails(ERROR, f"{symbol} :: Candle data missing. Using market order.")
            return None
        high = float(candles.loc[0, HIGH])
        return round(high * 1.001, 1) if float(ltp) < high else None
    except Exception as e:
        addLogDetails(ERROR, f"{symbol} :: Error fetching candle data: {e}. Using market order.")
        return None


# ---------------------------------------------------------------- flows


def triggerOrder(user_email, user_index_data, signal_data, order_type):
    strategy = signal_data.get(STRATEGY, "DefaultStrategy")
    index_name = user_index_data.get(INDEX_NAME)
    option_side = CE if str(order_type).upper() == BUY else PE
    alert = {"Strategy": strategy, "Index": index_name, "Signal": f"{order_type} ({option_side} entry)"}
    placed = False
    try:
        with _strategy_locks[(user_email, strategy)]:
            strategy_row = ManualOrders.objects.filter(
                user_id=user_email, index_name=index_name, strategy_name=strategy
            ).values().first()
            lots = int(
                strategy_row.get(LOTS)
                if strategy_row
                else signal_data.get(LOTS, user_index_data.get(LOTS, 1))
            )
            index_data = IndexDetails.objects.filter(index_name=index_name).values().first()
            if not index_data:
                raise Exception(f"Index data not found for {index_name}")
            qty = lots * int(index_data.get(QTY, 0))
            alert["Qty"] = qty

            position = _openPosition(user_email, strategy).values().first()
            if position:
                if option_side in position[SCRIPT_NAME].upper():
                    addLogDetails(INFO, f"{user_email} :: {order_type} order already exists")
                    return _response(True, "Message Exists")
                addLogDetails(INFO, f"{user_email} :: Reversal, exiting {position[SCRIPT_NAME]}")
                exitOrderWebhook(strategy, {INDEX_NAME: index_name, STRATEGY: strategy}, user_email)

            broker = Broker(user_email, INDIAN_INDEX).BrokerObject
            atm = broker.getCurrentAtm(index_name)
            alert["Spot ATM"] = atm
            if atm is None:
                raise Exception(f"[strike_calculation] atm=None for {index_name}")
            strike = int(user_index_data.get(STRIKE, 0))
            strike_price = atm - strike if option_side == CE else atm + strike
            prefix = getTradingSymbol(index_name)
            if not prefix:
                raise Exception(f"Could not build trading symbol for {index_name} (expiry missing?)")
            symbol = f"{prefix}{strike_price}{option_side}"
            exchange = _exchange(index_name)
            alert["Symbol"] = symbol

            ltp = broker.getLtpForPremium(broker.getCurrentPremiumDetails(exchange, symbol))
            if broker.is_demo_enabled:
                entry_price = ltp
            else:
                trigger = None
                if user_index_data.get(ON_CANDLE_CLOSE):
                    trigger = entryTrigger(broker, symbol, ltp, exchange, user_index_data.get(TIMEFRAME))
                order = buildOrder(
                    broker, symbol, BUY, qty, user_index_data.get(PRODUCT_TYPE), exchange, trigger
                )
                addLogDetails(INFO, f"{user_email} :: Placing {order_type.lower()} order for {symbol}")
                order_id, unique_order_id = placeAndVerify(broker, order, user_email)
                placed = True
                entry_price = trigger or fillPrice(broker, unique_order_id, ltp)
                addWebhookOrderDetails(
                    user_email,
                    index_name,
                    strategy,
                    {"current_premium": symbol, "order_id": order_id, "unique_order_id": unique_order_id},
                )

            addOrderBookDetails(
                {
                    USER_ID: user_email,
                    SCRIPT_NAME: symbol,
                    QTY: qty,
                    ENTRY_PRICE: entry_price,
                    STATUS: ORDER_PLACED,
                    STRATEGY: strategy,
                    INDEX_NAME: index_name,
                },
                True,
            )
            addLogDetails(INFO, f"{user_email} :: {order_type.capitalize()} order placed successfully")
            return _response(True, "Message Exits")

    except Exception as e:
        addLogDetails(ERROR, f"{user_email} :: triggerOrder error: {e}")
        symbol = alert.get("Symbol")
        if placed:
            title = "ENTRY PLACED BUT NOT SAVED - AUTO EXIT WILL NOT WORK"
            action = f"Position {symbol} is OPEN in AngelOne but not tracked. Exit it manually when the exit signal comes."
        else:
            title = "ENTRY SKIPPED - NO POSITION TAKEN"
            action = f"No order was sent. Take the {option_side} entry manually if you want this trade."
        sendTradeAlert(title, user_email, str(e), alert, action)
        return _response(False, "Unexpected error Check logs")


def exitOrderWebhook(strategy, data, user_email):
    index_name = (data or {}).get(INDEX_NAME)
    alert = {"Strategy": strategy, "Index": index_name}
    exit_placed = False
    try:
        with _strategy_locks[(user_email, strategy)]:
            position = _openPosition(user_email, strategy)
            info = position.values().first()
            if not info:
                addLogDetails(INFO, f"{user_email} :: No Pending orders for strategy {strategy}")
                return _response(False, "No pending Messages")

            symbol, qty, entry_price = info[SCRIPT_NAME], info[QTY], info[ENTRY_PRICE]
            exchange = _exchange(info.get(INDEX_NAME) or index_name)
            alert.update({"Symbol": symbol, "Qty": qty, "Entry price": entry_price})
            broker = Broker(user_email, INDIAN_INDEX).BrokerObject

            def close(exit_price):
                position.update(
                    **{
                        EXIT_TIME: getCurrentTimestamp(),
                        EXIT_PRICE: exit_price,
                        TOTAL: _pnl(exit_price, entry_price, qty),
                        STATUS: ORDER_EXITED,
                    }
                )

            if broker.is_demo_enabled:
                close(broker.getLtpForPremium(broker.getCurrentPremiumDetails(exchange, symbol)))
                return _response(True, "Message Done")

            webhook = _webhookDetails(user_email, index_name, strategy)
            if not webhook:
                raise Exception(f"No webhook data found for {strategy}")

            # Raises if the broker can't be reached: keep the entry, alert instead.
            status = broker.getOrderStatus(webhook.get(UNIQUE_ORDER_ID))
            alert["Entry order status"] = status

            if status == "complete":
                order = buildOrder(
                    broker, webhook.get(CURRENT_PREMIUM), SELL, qty,
                    _productType(user_email, index_name), exchange,
                )
                _, unique_order_id = placeAndVerify(broker, order, user_email)
                exit_placed = True
                ltp = broker.getLtpForPremium(broker.getCurrentPremiumDetails(exchange, symbol))
                close(fillPrice(broker, unique_order_id, ltp, entry_price))
            elif status in PENDING_STATUSES:
                _cancelPending(broker, webhook, status)
                addLogDetails(INFO, f"{user_email} :: Existing order cancelled.")
                position.delete()
            else:
                addLogDetails(INFO, f"{user_email} :: Entry order status '{status}', deleting entry.")
                position.delete()

        addLogDetails(INFO, f"{user_email} :: Order exited successfully.")
        return _response(True, "Message Done")

    except Exception as e:
        addLogDetails(ERROR, f"{user_email} :: exitOrderWebhook error: {e}")
        symbol = alert.get("Symbol")
        if exit_placed:
            title = "EXIT ORDER PLACED BUT NOT SAVED"
            action = f"Exit SELL for {symbol} was sent. Confirm in AngelOne that it is closed; the trade record was not updated."
        else:
            title = "EXIT FAILED - POSITION MAY STILL BE OPEN"
            action = f"Open AngelOne and exit {symbol} ({alert.get('Qty')} qty) manually NOW."
        sendTradeAlert(title, user_email, str(e), alert, action)
        return _response(False, "Unexpected error. Check logs.")


def modifyToMarketOrder(user_email, user_index_data, strategy, order_type):
    index_name = user_index_data.get(INDEX_NAME)
    alert = {"Strategy": strategy, "Index": index_name}
    placed = False
    try:
        with _strategy_locks[(user_email, strategy)]:
            broker = Broker(user_email, INDIAN_INDEX).BrokerObject
            if broker.is_demo_enabled:
                return JsonResponse({STATUS: SUCCESS, MESSAGE: "Demo Enabled", TASK_STATUS: True})

            position = _openPosition(user_email, strategy)
            info = position.values().first()
            if not info:
                addLogDetails(INFO, f"{user_email} :: No Pending orders for strategy {strategy}")
                return _response(False, "No pending Messages")

            webhook = _webhookDetails(user_email, index_name, strategy)
            if not webhook:
                raise Exception(f"Webhook details not found for {user_email}, strategy: {strategy}")

            symbol, qty = webhook.get(CURRENT_PREMIUM), int(info[QTY])
            alert.update({"Symbol": symbol, "Qty": qty})

            # Raises on API failure so we never fire a duplicate market BUY.
            status = broker.getOrderStatus(webhook.get(UNIQUE_ORDER_ID))
            alert["Entry order status"] = status
            if status == "complete":
                msg = f"Order already placed for ID {webhook.get(UNIQUE_ORDER_ID)}"
                addLogDetails(INFO, f"{user_email} :: {msg}")
                return JsonResponse({STATUS: SUCCESS, MESSAGE: msg, TASK_STATUS: True})
            if status in PENDING_STATUSES:
                _cancelPending(broker, webhook, status)

            order = buildOrder(
                broker, symbol, BUY, qty, _productType(user_email, index_name), _exchange(index_name)
            )
            order_id, unique_order_id = placeAndVerify(broker, order, user_email)
            placed = True
            position.update(
                **{ENTRY_PRICE: fillPrice(broker, unique_order_id, info[ENTRY_PRICE]), STATUS: ORDER_PLACED}
            )
            addWebhookOrderDetails(
                user_email,
                index_name,
                strategy,
                {"current_premium": symbol, "order_id": order_id, "unique_order_id": unique_order_id},
            )
            return _response(True, "Order placed successfully")

    except Exception as e:
        addLogDetails(ERROR, f"{user_email} :: modifyToMarketOrder error: {e}")
        symbol = alert.get("Symbol")
        if placed:
            title = "MARKET ENTRY PLACED BUT NOT SAVED - AUTO EXIT WILL NOT WORK"
            action = f"Position {symbol} is OPEN in AngelOne but not tracked. Exit it manually when the exit signal comes."
        else:
            title = "MARKET CONVERSION FAILED"
            action = f"Pending entry for {symbol} was not converted to market. Check AngelOne and enter/cancel manually."
        sendTradeAlert(title, user_email, str(e), alert, action)
        return _response(False, "Unexpected error. Check logs.")
