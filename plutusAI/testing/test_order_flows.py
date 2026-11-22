"""Behaviour of entry / exit / convert-to-market order flows (broker faked)."""
from django.test import TestCase

from plutusAI.models import IndexDetails, ManualOrders, OrderBook, WebhookDetails
from plutusAI.server import manualOrder
from plutusAI.server.constants import BUY, SELL
from plutusAI.testing.fakes import USER, FakeBroker, patch_order_env

STRATEGY = "ST_target"


class OrderFlowTestCase(TestCase):
    def setUp(self):
        IndexDetails.objects.create(
            index_name="nifty", index_token="99926000", ltp="0",
            last_updated_time="0", qty="65", current_expiry="03-Nov-2026",
            next_expiry="09-Nov-2026",
        )
        ManualOrders.objects.create(
            user_id=USER, index_name="nifty", strike="100", lots="1",
            strategy_name=STRATEGY,
        )

    def use(self, **kwargs):
        self.broker = FakeBroker(**kwargs)
        self.alerts = patch_order_env(self, self.broker)
        return self.broker

    def user_index_data(self):
        return ManualOrders.objects.filter(user_id=USER).values().first()

    def entry(self, order_type):
        manualOrder.triggerOrder(USER, self.user_index_data(),
                                 {"strategy": STRATEGY}, order_type)

    def open_position(self, symbol="NIFTY03NOV2622400CE"):
        OrderBook.objects.create(
            user_id=USER, entry_time="1", script_name=symbol, qty="65",
            entry_price="100.0", status="order_placed", strategy=STRATEGY,
            index_name="nifty",
        )
        WebhookDetails.objects.create(
            user_id=USER, index_name="nifty", strategy=STRATEGY,
            order_status="order_placed", time="1", order_id="OID0",
            unique_order_id="UID0", current_premium=symbol,
        )

    def exit(self):
        manualOrder.exitOrderWebhook(STRATEGY, {"index_name": "nifty"}, USER)

    def open_rows(self):
        return OrderBook.objects.filter(user_id=USER, exit_price=None)


class EntryTests(OrderFlowTestCase):
    def test_buy_signal_places_ce_below_atm_and_records_it(self):
        broker = self.use()
        self.entry(BUY)
        self.assertEqual(len(broker.placed), 1)
        order = broker.placed[0]
        self.assertEqual(order["tradingsymbol"], "NIFTY03NOV2622400CE")
        self.assertEqual(order["transactiontype"], BUY)
        self.assertEqual(order["ordertype"], "MARKET")
        self.assertEqual(order["quantity"], 65)
        row = self.open_rows().get()
        self.assertEqual(row.script_name, "NIFTY03NOV2622400CE")
        self.assertEqual(float(row.entry_price), 101.5)
        self.assertEqual(
            WebhookDetails.objects.get(user_id=USER).unique_order_id, "UID1"
        )
        self.assertEqual(self.alerts, [])

    def test_sell_signal_places_pe_above_atm(self):
        broker = self.use()
        self.entry(SELL)
        self.assertEqual(broker.placed[0]["tradingsymbol"], "NIFTY03NOV2622600PE")

    def test_broker_rejection_records_nothing_and_alerts(self):
        self.use(place_ok=False)
        self.entry(BUY)
        self.assertFalse(self.open_rows().exists())
        self.assertEqual(self.alerts, ["ENTRY SKIPPED - NO POSITION TAKEN"])

    def test_missing_spot_price_skips_entry_and_alerts(self):
        broker = self.use(atm=None)
        self.entry(BUY)
        self.assertEqual(broker.placed, [])
        self.assertEqual(self.alerts, ["ENTRY SKIPPED - NO POSITION TAKEN"])

    def test_demo_mode_records_at_ltp_without_broker_order(self):
        broker = self.use(demo=True, ltp="99.0")
        self.entry(BUY)
        self.assertEqual(broker.placed, [])
        self.assertEqual(self.open_rows().get().entry_price, "99.0")

    def test_same_direction_signal_with_open_position_is_ignored(self):
        broker = self.use()
        self.open_position("NIFTY03NOV2622400CE")
        self.entry(BUY)
        self.assertEqual(broker.placed, [])
        self.assertEqual(self.open_rows().count(), 1)

    def test_opposite_signal_exits_ce_then_enters_pe(self):
        broker = self.use()
        self.open_position("NIFTY03NOV2622400CE")
        self.entry(SELL)
        sides = [(o["transactiontype"], o["tradingsymbol"]) for o in broker.placed]
        self.assertEqual(sides, [(SELL, "NIFTY03NOV2622400CE"),
                                 (BUY, "NIFTY03NOV2622600PE")])
        self.assertEqual(self.open_rows().get().script_name, "NIFTY03NOV2622600PE")


class ExitTests(OrderFlowTestCase):
    def test_filled_entry_is_sold_and_marked_exited(self):
        broker = self.use(order_status="complete")
        self.open_position()
        self.exit()
        self.assertEqual(broker.placed[0]["transactiontype"], SELL)
        self.assertEqual(broker.placed[0]["quantity"], "65")
        self.assertFalse(self.open_rows().exists())
        self.assertEqual(OrderBook.objects.get().status, "order_exited")

    def test_exit_does_not_wait_for_ltp_before_selling(self):
        broker = self.use(order_status="complete", ltp="Internet connection issue")
        self.open_position()
        self.exit()
        self.assertEqual(broker.placed[0]["transactiontype"], SELL)
        self.assertEqual(OrderBook.objects.get().exit_price, "101.5")  # broker fill
        self.assertEqual(self.alerts, [])

    def test_pending_entry_is_cancelled_and_removed(self):
        broker = self.use(order_status="trigger pending")
        self.open_position()
        self.exit()
        self.assertEqual(broker.placed, [])
        self.assertEqual(broker.cancelled, ["OID0"])
        self.assertFalse(OrderBook.objects.exists())

    def test_rejected_entry_is_removed_without_order(self):
        broker = self.use(order_status="rejected")
        self.open_position()
        self.exit()
        self.assertEqual(broker.placed, [])
        self.assertFalse(OrderBook.objects.exists())

    def test_unknown_status_keeps_position_and_alerts(self):
        broker = self.use(order_status=Exception("Read timed out"))
        self.open_position()
        self.exit()
        self.assertEqual(broker.placed, [])
        self.assertEqual(self.open_rows().count(), 1)
        self.assertEqual(self.alerts, ["EXIT FAILED - POSITION MAY STILL BE OPEN"])

    def test_rejected_exit_keeps_position_and_alerts(self):
        self.use(order_status="complete", place_ok=False)
        self.open_position()
        self.exit()
        self.assertEqual(self.open_rows().count(), 1)
        self.assertEqual(self.alerts, ["EXIT FAILED - POSITION MAY STILL BE OPEN"])

    def test_no_open_position_does_nothing(self):
        broker = self.use()
        self.exit()
        self.assertEqual(broker.placed, [])
        self.assertEqual(self.alerts, [])

    def test_demo_exit_books_pnl_at_ltp(self):
        self.use(demo=True, ltp="110.0")
        self.open_position()
        self.exit()
        row = OrderBook.objects.get()
        self.assertEqual(row.exit_price, "110.0")
        self.assertEqual(float(row.total), 650.0)


class ModifyToMarketTests(OrderFlowTestCase):
    def modify(self):
        manualOrder.modifyToMarketOrder(USER, {"index_name": "nifty"}, STRATEGY, BUY)

    def test_filled_entry_is_left_alone(self):
        broker = self.use(order_status="complete")
        self.open_position()
        self.modify()
        self.assertEqual(broker.placed, [])

    def test_unfilled_entry_is_cancelled_and_replaced_by_market_buy(self):
        broker = self.use(order_status="trigger pending")
        self.open_position()
        self.modify()
        self.assertEqual(broker.cancelled, ["OID0"])
        self.assertEqual(len(broker.placed), 1)
        self.assertEqual(broker.placed[0]["ordertype"], "MARKET")
        # OrderBook qty is already lots * lot size; it must not be multiplied again.
        self.assertEqual(broker.placed[0]["quantity"], 65)
        row = self.open_rows().get()  # same row updated, no duplicate
        self.assertEqual(float(row.entry_price), 101.5)
        self.assertEqual(WebhookDetails.objects.get().unique_order_id, "UID1")

    def test_unknown_status_places_nothing_and_alerts(self):
        broker = self.use(order_status=Exception("Read timed out"))
        self.open_position()
        self.modify()
        self.assertEqual(broker.placed, [])
        self.assertEqual(self.alerts, ["MARKET CONVERSION FAILED"])
