"""Fake broker used by tests: records every call, never touches the network."""
import logging
from unittest import mock

USER = "trader@test.in"
SYMBOL_PREFIX = "NIFTY03NOV26"


class FakeBroker:
    def __init__(self, atm=22500, ltp="100.0", order_status="complete",
                 place_ok=True, demo=False):
        self.is_demo_enabled = demo
        self.atm = atm
        self.ltp = ltp
        self.order_status = order_status  # str, or Exception to raise
        self.place_ok = place_ok
        self.placed = []
        self.cancelled = []

    # --- market data ---
    def getCurrentAtm(self, index_name):
        return self.atm

    def getCurrentPremiumDetails(self, exchange, symbol):
        return {"exchange": exchange, "tradingsymbol": symbol, "symboltoken": "123"}

    def getLtpForPremium(self, option_details):
        return self.ltp

    def getTokenForSymbol(self, symbol):
        return "123"

    def getCandleData(self, *args):
        return None

    # --- orders ---
    def placeOrder(self, order_details):
        self.placed.append(dict(order_details))
        if not self.place_ok:
            return {"status": False, "message": "Invalid symboltoken",
                    "errorcode": "AB4033", "data": None}
        n = len(self.placed)
        return {"status": True, "message": "SUCCESS", "errorcode": "",
                "data": {"orderid": f"OID{n}", "uniqueorderid": f"UID{n}"}}

    def getOrderDetails(self, unique_order_id):
        return {"price": 101.5, "triggerprice": 0.0, "averageprice": 101.5}

    def getOrderStatus(self, unique_order_id):
        if isinstance(self.order_status, Exception):
            raise self.order_status
        return self.order_status

    def cancelOrder(self, order_id, variety):
        self.cancelled.append(order_id)

    # --- account / forex ---
    def checkProfile(self):
        return {"message": "SUCCESS", "errorcode": ""}

    def placeOrderForex(self, side, data):
        self.placed.append({"forex_side": side, **data})
        return {"ticket": len(self.placed)}

    def exitOrderForex(self, data):
        self.placed.append({"forex_exit": True, **data})
        return {"closed": True}


class BrokerFactory:
    """Stands in for the Broker class: Broker(email, group).BrokerObject."""

    def __init__(self, broker):
        self.broker = broker
        self.is_demo_enabled = broker.is_demo_enabled

    def __call__(self, *args, **kwargs):
        return self

    @property
    def BrokerObject(self):
        return self.broker


def patch_order_env(test, broker, module="plutusAI.server.manualOrder"):
    """Patches broker, trading symbol and Telegram for one test; returns alerts list."""
    logging.disable(logging.CRITICAL)
    test.addCleanup(logging.disable, logging.NOTSET)
    alerts = []
    patches = [
        mock.patch(f"{module}.Broker", BrokerFactory(broker)),
        mock.patch(f"{module}.getTradingSymbol", lambda index: SYMBOL_PREFIX),
        mock.patch(f"{module}.sendTradeAlert",
                   lambda title, *a, **k: alerts.append(title)),
    ]
    for p in patches:
        p.start()
        test.addCleanup(p.stop)
    return alerts
