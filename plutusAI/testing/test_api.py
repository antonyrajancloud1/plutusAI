"""Every HTTP endpoint: access control plus the normal (happy) path.

External effects are faked: broker, Celery, subprocess (ps/pkill), AngelOne login,
NSE expiry fetch and Telegram. Webhook background jobs run inline so the whole
signal -> order -> OrderBook path is exercised.
"""
import json
import logging
from types import SimpleNamespace
from unittest import mock

from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework.authtoken.models import Token

from plutusAI.models import (
    BrokerDetails, Configuration, FlashDetails, IndexDetails, JobDetails, LogDetails,
    ManualOrders, OrderBook, PaymentDetails, ScalperDetails, TelegramBotConfig,
    TelegramSettings,
)
from plutusAI.server import manualOrder
from plutusAI.testing.fakes import BrokerFactory, FakeBroker

USER, ADMIN = "trader@test.in", "boss@test.in"
PAGES = ["/home", "/dashboard", "/manual", "/view_logs"]


class ApiTestCase(TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.addCleanup(logging.disable, logging.NOTSET)
        self.broker = FakeBroker(demo=True, ltp="100.0")
        self.alerts, self.ps_output = [], ""
        factory = BrokerFactory(self.broker)
        ps = lambda *a, **k: SimpleNamespace(stdout=self.ps_output, returncode=0)
        self.popen = mock.MagicMock()
        self.delay = mock.MagicMock(return_value=SimpleNamespace(id="job-1"))
        for target, value in [
            ("plutusAI.server.manualOrder.Broker", factory),
            ("plutusAI.views.orders.Broker", factory),
            ("plutusAI.views.admin.Broker", factory),
            ("plutusAI.server.manualOrder.getTradingSymbol", lambda index: "NIFTY03NOV26"),
            ("plutusAI.server.manualOrder.sendTradeAlert", lambda t, *a, **k: self.alerts.append(t)),
            ("plutusAI.server.api.sendTradeAlert", lambda t, *a, **k: self.alerts.append(t)),
            ("plutusAI.views.admin.subprocess.run", ps),
            ("plutusAI.views.admin.subprocess.Popen", self.popen),
            ("plutusAI.views.admin.time.sleep", lambda s: None),
            ("plutusAI.views.admin.AngelOneAuth", mock.MagicMock()),
            ("plutusAI.views.admin.updateExpiryDetails", mock.MagicMock()),
            ("celery.app.task.Task.delay", self.delay),
            ("celery.result.AsyncResult.revoke", mock.MagicMock()),
            ("plutusAI.server.telegram_notifier.requests.post", mock.MagicMock()),
        ]:
            patcher = mock.patch(target, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        # Run webhook background jobs inline.
        patcher = mock.patch.object(manualOrder.executor, "submit", lambda fn, *a: fn(*a))
        patcher.start()
        self.addCleanup(patcher.stop)

        IndexDetails.objects.create(
            index_name="nifty", index_token="99926000", ltp="0", last_updated_time="0",
            qty="65", current_expiry="03-Nov-2026", next_expiry="09-Nov-2026",
        )
        self.admin_user = User.objects.create_user("boss", ADMIN, "pw", is_staff=True)
        self.admin = Client()
        self.admin.force_login(self.admin_user)
        resp = self.call(self.admin, "post", "/add_user", {"email": USER, "password": "pw"})
        self.assertEqual(resp["message"], "User added")
        self.user_obj = User.objects.get(email=USER)
        self.user = Client()
        self.user.force_login(self.user_obj)
        self.anon = Client()
        self.user_token = Token.objects.create(user=self.user_obj).key
        self.admin_token = Token.objects.create(user=self.admin_user).key

    def call(self, client, method, url, body=None, status=200):
        if method == "get":
            resp = client.get(url, body or {})
        else:
            resp = getattr(client, method)(url, json.dumps(body or {}), content_type="application/json")
        self.assertEqual(resp.status_code, status, f"{method.upper()} {url}: {resp.content[:300]}")
        return resp.json() if resp.get("Content-Type", "").startswith("application/json") else resp


class AccessControlTests(ApiTestCase):
    SESSION_APIS = [
        ("get", "/get_config_values"), ("put", "/update_config_values"),
        ("get", "/get_scalper_details"), ("put", "/update_scalper_details"),
        ("get", "/get_flash_details"), ("put", "/update_flash_details"),
        ("get", "/manual_details"), ("put", "/update_manual_details"),
        ("get", "/get_strategy_details"), ("post", "/add_strategy_details"),
        ("put", "/update_strategy_details"), ("post", "/delete_strategy_details"),
        ("get", "/get_broker_details"), ("post", "/add_broker_details"),
        ("put", "/edit_broker_details"), ("get", "/get_telegram_settings"),
        ("post", "/update_telegram_settings"), ("post", "/place_order_buy"),
        ("post", "/place_order_sell"), ("post", "/place_order_exit"),
        ("get", "/get_order_book_details"), ("get", "/all_open_orders"),
        ("get", "/get_strategy_summary"), ("post", "/start_index"),
        ("post", "/start_scalper"), ("post", "/start_flash"), ("post", "/stop_index"),
        ("get", "/check_task_status"), ("get", "/get_celery_status"), ("get", "/plans"),
        ("post", "/get_auth_token"), ("post", "/generate_auth_token"), ("get", "/check_admin"),
        ("post", "/regenerate_token"), ("get", "/check_broker_status"),
        ("get", "/get_index_data"), ("get", "/get_log_details"), ("get", "/logout"),
    ]
    ADMIN_APIS = [
        ("post", "/add_user"), ("put", "/edit_plans"), ("post", "/start_ws"),
        ("post", "/stop_ws"), ("post", "/stop_celery"), ("post", "/restart_celery"),
        ("get", "/get_telegram_bot_config"), ("post", "/update_telegram_bot_config"),
    ]
    TOKEN_APIS = ["/trigger_buy", "/trigger_sell", "/trigger_exit", "/trigger_order_to_market",
                  "/forex_buy_order", "/forex_sell_order", "/forex_close_order"]
    ADMIN_TOKEN_APIS = ["/exit_all", "/update_expiry_details"]

    def test_anonymous_gets_unauthorised_from_every_api(self):
        for method, url in self.SESSION_APIS + self.ADMIN_APIS:
            with self.subTest(url=url):
                self.assertEqual(self.call(self.anon, method, url)["message"], "unauthorised")

    def test_normal_user_cannot_use_admin_apis(self):
        for method, url in self.ADMIN_APIS:
            with self.subTest(url=url):
                self.assertEqual(self.call(self.user, method, url)["message"], "unauthorised")
        self.assertFalse(User.objects.filter(email="x@test.in").exists())
        self.popen.assert_not_called()

    def test_webhooks_reject_missing_or_wrong_token(self):
        for url in self.TOKEN_APIS + self.ADMIN_TOKEN_APIS:
            with self.subTest(url=url):
                self.call(self.anon, "post", url, {"index_name": "nifty"}, status=401)
                self.call(self.anon, "post", f"{url}?token=wrong", {"index_name": "nifty"}, status=401)

    def test_admin_token_webhooks_reject_normal_user_token(self):
        for url in self.ADMIN_TOKEN_APIS:
            with self.subTest(url=url):
                resp = self.call(self.anon, "post", f"{url}?token={self.user_token}")
                self.assertEqual(resp["message"], "unauthorised")

    def test_wrong_http_method_is_rejected(self):
        self.call(self.user, "get", "/place_order_buy", status=405)
        self.call(self.user, "post", "/get_config_values", status=405)

    def test_pages_redirect_anonymous_to_login_and_render_for_users(self):
        for url in PAGES + ["/admin_console", "/"]:
            with self.subTest(url=url):
                self.assertEqual(self.anon.get(url).url, "/login")
        self.assertEqual(self.user.get("/dashboard").status_code, 200)
        self.assertTemplateUsed(self.user.get("/dashboard"), "dashboard.html")
        self.assertEqual(self.user.get("/").url, "/dashboard")

    def test_old_page_urls_open_the_matching_dashboard_section(self):
        for url, section in [("/home", "dashboard"), ("/manual", "manual"),
                             ("/view_logs", "logs"), ("/admin_console", "admin")]:
            with self.subTest(url=url):
                self.assertEqual(self.user.get(url).url, f"/dashboard#/{section}")


class LoginTests(ApiTestCase):
    def test_login_page_and_credentials(self):
        self.assertEqual(self.anon.get("/login").status_code, 200)
        bad = self.anon.post("/login", {"user_name": "trader", "password": "nope"}).json()
        self.assertEqual(bad["message"], "error_in_login")
        good = self.anon.post("/login", {"user_name": "trader", "password": "pw"}).json()
        self.assertEqual(good["message"], "login_success")
        self.assertEqual(self.anon.get("/login").url, "/dashboard")  # already logged in

    def test_missing_fields_fail_cleanly(self):
        self.assertEqual(self.anon.post("/login", {}).json()["message"], "error_in_login")

    def test_logout(self):
        self.assertEqual(self.call(self.user, "get", "/logout")["message"], "logout_success")
        self.assertEqual(self.call(self.user, "get", "/check_admin")["message"], "unauthorised")


class ConfigTests(ApiTestCase):
    def test_strategy_configs_read_and_update(self):
        for model, get_url, put_url, change, message in [
            (Configuration, "/get_config_values", "/update_config_values", {"lots": "3", "levels": "1,2"}, "config_values_updated"),
            (ScalperDetails, "/get_scalper_details", "/update_scalper_details", {"lots": "4"}, "scalper_details_updated"),
            (FlashDetails, "/get_flash_details", "/update_flash_details", {"lots": "5"}, "flash_details_updated"),
        ]:
            with self.subTest(url=put_url):
                index = model.objects.filter(user_id=USER).first().index_name
                one = self.call(self.user, "get", get_url, {"index_name": index})
                self.assertNotIn("user_id", one)
                self.assertIsInstance(self.call(self.user, "get", get_url), dict)
                resp = self.call(self.user, "put", put_url, {"index_name": index, **change})
                self.assertEqual(resp["message"], message)
                self.assertEqual(model.objects.get(user_id=USER, index_name=index).lots, change["lots"])

    def test_unknown_index_returns_not_found(self):
        for url in ("/get_config_values", "/get_scalper_details", "/get_flash_details"):
            with self.subTest(url=url):
                resp = self.call(self.user, "get", url, {"index_name": "nope"})
                self.assertEqual(resp["message"], "index_details_not_found")
        for url in ("/update_config_values", "/update_scalper_details", "/update_flash_details"):
            with self.subTest(url=url):
                resp = self.call(self.user, "put", url, {"index_name": "nope", "lots": "1"})
                self.assertEqual(resp["message"], "index_details_not_found")

    def test_validation_errors_return_400(self):
        index = Configuration.objects.filter(user_id=USER).first().index_name
        resp = self.call(self.user, "put", "/update_config_values", {"index_name": index, "lots": "abc"}, status=400)
        self.assertEqual(resp["status"], "failed")

    def test_cannot_reassign_rows_to_another_user(self):
        index = ScalperDetails.objects.filter(user_id=USER).first().index_name
        self.call(self.user, "put", "/update_scalper_details", {"index_name": index, "user_id": ADMIN})
        self.assertFalse(ScalperDetails.objects.filter(user_id=ADMIN).exists())

    def test_manual_settings_read_and_update(self):
        rows = self.call(self.user, "get", "/manual_details")["message"]
        self.assertTrue(rows)
        resp = self.call(self.user, "put", "/update_manual_details",
                         {"index_name": "nifty", "lots": "2", "strategy_name": "hacked"})
        self.assertEqual(resp["message"], "config_values_updated")
        row = ManualOrders.objects.get(user_id=USER, index_name="nifty")
        self.assertEqual((row.lots, row.strategy_name), ("2", None))
        self.assertEqual(self.call(self.user, "get", "/manual_details", {"index_name": "zzz"})["message"],
                         "index_details_not_found")

    def test_strategy_crud(self):
        add = {"strategy_name": "ST_target", "index_name": "nifty", "strike": "100", "lots": "1"}
        self.assertEqual(self.call(self.user, "post", "/add_strategy_details", add)["message"], "Strategy added")
        self.assertIn("already exists", self.call(self.user, "post", "/add_strategy_details", add)["message"])
        self.assertIn("mandatory", self.call(self.user, "post", "/add_strategy_details", {})["message"])

        names = [s["strategy_name"] for s in self.call(self.user, "get", "/get_strategy_details")["data"]]
        self.assertIn("ST_target", names)

        upd = {"strategy_name": "ST_target", "fields": {"lots": "7", "user_id": ADMIN}}
        self.assertEqual(self.call(self.user, "put", "/update_strategy_details", upd)["message"], "Updated successfully")
        self.assertEqual(ManualOrders.objects.get(strategy_name="ST_target").lots, "7")
        self.assertEqual(ManualOrders.objects.get(strategy_name="ST_target").user_id, USER)
        self.assertEqual(self.call(self.user, "put", "/update_strategy_details", {})["message"], "Invalid request")

        self.assertEqual(self.call(self.user, "post", "/delete_strategy_details",
                                   {"strategy_name": "ST_target"})["message"], "Deleted successfully")
        self.assertEqual(self.call(self.user, "post", "/delete_strategy_details",
                                   {"strategy_name": "ST_target"})["message"], "No record found")

    def test_broker_details(self):
        self.assertTrue(self.call(self.user, "get", "/get_broker_details")["broker_details"])
        one = self.call(self.user, "get", "/get_broker_details", {"broker_name": "angel_one"})
        self.assertEqual(one["broker_details"]["broker_name"], "angel_one")

        resp = self.call(self.user, "put", "/edit_broker_details",
                         {"index_group": "indian_index", "broker_mpin": "9999"})
        self.assertEqual(resp["message"], "broker_details_updated")
        self.assertEqual(BrokerDetails.objects.get(user_id=USER).broker_mpin, "9999")
        self.call(self.user, "put", "/edit_broker_details", {"index_group": "indian_index", "broker_mpin": "bad!"}, status=400)

        self.assertIn("Missing fields", self.call(self.user, "post", "/add_broker_details", {})["message"])
        forex = {"user_id": USER, "broker_name": "exness", "broker_user_id": "E1", "is_demo_trading_enabled": True,
                 "broker_password": "x", "broker_forex_server": "srv"}
        self.assertEqual(self.call(self.user, "post", "/add_broker_details", forex)["message"], "broker_details_added")
        self.assertEqual(BrokerDetails.objects.get(broker_name="exness").index_group, "forex")

    def test_telegram_settings(self):
        self.assertEqual(self.call(self.user, "get", "/get_telegram_settings")["chat_id"], "")
        resp = self.call(self.user, "post", "/update_telegram_settings", {"chat_id": " 123 ", "notify_on_error": True})
        self.assertEqual((resp["chat_id"], resp["notify_on_error"]), ("123", True))
        self.assertTrue(TelegramSettings.objects.get(user_id=USER).notify_on_error)


class OrderEndpointTests(ApiTestCase):
    def webhook(self, url, body, token=None):
        return self.call(self.anon, "post", f"{url}?token={token or self.user_token}", body)

    def test_manual_buy_then_exit_records_trade(self):
        self.assertEqual(self.call(self.user, "post", "/place_order_buy", {"index_name": "nifty"})["message"],
                         "Message Exists BUY")
        row = OrderBook.objects.get(user_id=USER)
        self.assertEqual(row.script_name, "NIFTY03NOV2622400CE")
        self.broker.ltp = "120.0"
        self.assertEqual(self.call(self.user, "post", "/place_order_exit", {"index_name": "nifty"})["message"],
                         "Message Done")
        row.refresh_from_db()
        self.assertEqual((row.exit_price, float(row.total)), ("120.0", 1300.0))

    def test_manual_buy_reports_failure_when_entry_fails(self):
        self.broker.atm = None
        resp = self.call(self.user, "post", "/place_order_buy", {"index_name": "nifty"})
        self.assertEqual(resp["status"], "failed")
        self.assertEqual(self.alerts, ["ENTRY SKIPPED - NO POSITION TAKEN"])

    def test_manual_exit_without_position_says_so(self):
        resp = self.call(self.user, "post", "/place_order_exit", {"index_name": "nifty"})
        self.assertEqual(resp["message"], "No pending Messages")

    def test_manual_sell_takes_pe(self):
        self.call(self.user, "post", "/place_order_sell", {"index_name": "nifty"})
        self.assertTrue(OrderBook.objects.get(user_id=USER).script_name.endswith("22600PE"))

    def test_webhook_buy_sell_exit_flow(self):
        body = {"index_name": "nifty", "strategy": "ST_target"}
        self.assertEqual(self.webhook("/trigger_buy", body)["message"], "Message Done")
        self.assertTrue(OrderBook.objects.get(exit_price=None).script_name.endswith("CE"))
        self.webhook("/trigger_sell", body)  # reversal: exit CE, enter PE
        self.assertTrue(OrderBook.objects.get(exit_price=None).script_name.endswith("PE"))
        self.assertEqual(self.webhook("/trigger_exit", body)["message"], "Message Exists SELL")
        self.assertFalse(OrderBook.objects.filter(exit_price=None).exists())
        self.assertEqual(OrderBook.objects.count(), 2)
        logs = list(LogDetails.objects.values_list("log", flat=True))
        self.assertEqual(len(logs), 3)
        self.assertIn("Buy Order triggered for strategy ST_target", logs)

    def test_webhook_for_unknown_index_alerts_instead_of_crashing(self):
        resp = self.webhook("/trigger_buy", {"index_name": "unknown"})
        self.assertEqual(resp["message"], "internal_error")
        self.assertEqual(self.alerts, ["ENTRY SIGNAL FAILED - NO POSITION TAKEN"])

    def test_convert_to_market_in_demo_mode_is_a_no_op(self):
        resp = self.webhook("/trigger_order_to_market", {"index_name": "nifty", "strategy": "ST_target"})
        self.assertEqual(resp["message"], "Modified")
        self.assertEqual(self.broker.placed, [])

    def test_exit_all_closes_every_open_position(self):
        for user, strategy in ((USER, "a"), (USER, "b")):
            OrderBook.objects.create(user_id=user, entry_time="1", script_name="NIFTY03NOV2622400CE",
                                     qty="65", entry_price="100", status="order_placed",
                                     strategy=strategy, index_name="nifty")
        resp = self.call(self.anon, "post", f"/exit_all?token={self.admin_token}")
        self.assertEqual(resp["message"], "done for the day")
        self.assertFalse(OrderBook.objects.filter(exit_price=None).exists())
        self.assertEqual(self.call(self.anon, "post", f"/exit_all?token={self.admin_token}")["message"],
                         "No open orders to exit")

    def test_order_book_open_orders_and_summary(self):
        self.call(self.user, "post", "/place_order_buy", {"index_name": "nifty"})
        book = self.call(self.user, "get", "/get_order_book_details")["order_book_details"]
        self.assertEqual((len(book), book[0]["exit_price"]), (1, ""))
        self.assertNotIn("id", book[0])
        open_orders = self.call(self.user, "get", "/all_open_orders")["open_orders"]
        self.assertEqual(open_orders[0]["ltp"], "100.0")
        summary = self.call(self.user, "get", "/get_strategy_summary")
        self.assertTrue(summary["task_status"])
        self.assertEqual(summary["summary"]["user_name"], "trader")

    def test_forex_webhooks(self):
        body = {"symbol": "XAUUSD", "volume": 0.1}
        self.assertEqual(self.webhook("/forex_buy_order", body)["message"], "Buy Completed")
        self.assertEqual(self.webhook("/forex_sell_order", body)["message"], {"ticket": 2})
        self.assertEqual(self.webhook("/forex_close_order", body)["message"], {"closed": True})
        self.assertEqual([o.get("forex_side") for o in self.broker.placed[:2]], [0, 1])


class AdminEndpointTests(ApiTestCase):
    def test_start_and_stop_strategy_jobs(self):
        for url, label in (("/start_index", "Nifty started"), ("/start_scalper", "Nifty scalper started"),
                           ("/start_flash", "Nifty flash started")):
            with self.subTest(url=url):
                self.assertEqual(self.call(self.user, "post", url, {"index_name": "nifty"})["message"], label)
        self.assertEqual(self.delay.call_count, 3)

        JobDetails.objects.create(user_id=USER, index_name="nifty", job_id="job-1", strategy="hunter")
        self.assertEqual(self.call(self.user, "post", "/start_index", {"index_name": "nifty"})["message"],
                         "Nifty process running")
        stop = self.call(self.user, "post", "/stop_index", {"index_name": "nifty", "strategy": "hunter"})
        self.assertEqual(stop["message"], "Index Stopped")
        self.assertFalse(JobDetails.objects.exists())
        self.assertEqual(self.call(self.user, "post", "/stop_index", {"index_name": "nifty", "strategy": "hunter"})["message"],
                         "Index not running")

    def test_stopping_each_strategy_marks_only_its_own_config_stopped(self):
        for model, strategy in ((Configuration, "hunter"), (ScalperDetails, "scalper"), (FlashDetails, "flash")):
            with self.subTest(strategy=strategy):
                index = model.objects.filter(user_id=USER).first().index_name
                for m in (Configuration, ScalperDetails, FlashDetails):
                    m.objects.filter(user_id=USER).update(status="running")
                JobDetails.objects.create(user_id=USER, index_name=index, job_id=f"job-{strategy}", strategy=strategy)
                stop = self.call(self.user, "post", "/stop_index", {"index_name": index, "strategy": strategy})
                self.assertEqual(stop["message"], "Index Stopped")
                self.assertEqual(model.objects.get(user_id=USER, index_name=index).status, "stopped")
                for m in {Configuration, ScalperDetails, FlashDetails} - {model}:
                    self.assertEqual(set(m.objects.filter(user_id=USER).values_list("status", flat=True)),
                                     {"running"}, m.__name__)

    def test_websocket_jobs(self):
        self.assertEqual(self.call(self.admin, "post", "/start_ws", {"ws_type": "9"})["message"], "Invalid ws_type")
        self.assertEqual(self.call(self.admin, "post", "/start_ws", {"ws_type": "1"})["message"], "WS started")
        JobDetails.objects.create(user_id="madara@plutus.com", index_name="socket_job", job_id="j", strategy="socket_job")
        self.assertEqual(self.call(self.admin, "post", "/start_ws", {"ws_type": "1"})["message"], "Socket running")
        self.assertEqual(self.call(self.user, "get", "/check_task_status")["message"], "Socket running")
        self.assertEqual(self.call(self.admin, "post", "/stop_ws", {"ws_type": "1"})["message"], "Index Stopped")
        self.assertEqual(self.call(self.user, "get", "/check_task_status")["message"], "No Socket Job Present")

    def test_celery_control(self):
        self.assertFalse(self.call(self.user, "get", "/get_celery_status")["celery_running"])
        self.assertEqual(self.call(self.admin, "post", "/stop_celery")["message"], "Celery is not running.")
        self.assertTrue(self.call(self.admin, "post", "/restart_celery")["success"])
        self.assertIn("celery -A plutus.celery worker", self.popen.call_args[0][0])
        self.ps_output = "madara 1 celery -A plutus.celery worker"
        self.assertTrue(self.call(self.user, "get", "/get_celery_status")["celery_running"])
        self.assertEqual(self.call(self.admin, "post", "/stop_celery")["message"], "Celery stopped successfully.")

    def test_add_user_and_plans(self):
        self.assertEqual(self.call(self.admin, "post", "/add_user", {"email": USER, "password": "pw"})["message"],
                         "user_already_present")
        self.assertIn("Missing", self.call(self.admin, "post", "/add_user", {})["message"])
        resp = self.call(self.admin, "put", "/edit_plans", {"user_id": USER, "renew_date": "30", "opted_index": "nifty"})
        self.assertEqual(resp["status"], "success")
        self.assertEqual(PaymentDetails.objects.get(user_id=USER).opted_index, "nifty")
        self.assertEqual(self.call(self.user, "get", "/plans")["plan_details"][0]["opted_index"], "nifty")

    def test_api_tokens(self):
        key = self.call(self.user, "post", "/get_auth_token")["message"]
        self.assertEqual(key, self.user_token)
        new_key = self.call(self.user, "post", "/generate_auth_token")["message"]
        self.assertNotEqual(new_key, key)
        self.call(self.anon, "post", f"/trigger_exit?token={key}", {"index_name": "nifty"}, status=401)

    def test_admin_flag_broker_session_and_index_data(self):
        self.assertFalse(self.call(self.user, "get", "/check_admin")["is_admin"])
        self.assertTrue(self.call(self.admin, "get", "/check_admin")["is_admin"])
        self.assertEqual(self.call(self.user, "post", "/regenerate_token")["message"], "token_generated")
        self.assertEqual(self.call(self.user, "get", "/check_broker_status")["message"], "token_is_valid")
        index = self.call(self.user, "get", "/get_index_data")["message"]["index_data"]
        self.assertEqual(index[0]["index_name"], "nifty")
        resp = self.call(self.anon, "post", f"/update_expiry_details?token={self.admin_token}")
        self.assertEqual(resp["message"], "Expiry details Updated")

    def test_broker_session_failure_reports_invalid_token(self):
        with mock.patch("plutusAI.views.admin.Broker", side_effect=Exception("down")):
            self.assertEqual(self.call(self.user, "get", "/check_broker_status")["message"], "token_is_invalid")

    def test_telegram_bot_config(self):
        self.assertEqual(self.call(self.admin, "get", "/get_telegram_bot_config")["bot_id"], "")
        resp = self.call(self.admin, "post", "/update_telegram_bot_config",
                         {"bot_id": " b1 ", "admin_bot_id": "b2", "admin_chat_ids": "1,2"})
        self.assertEqual((resp["bot_id"], resp["admin_chat_ids"]), ("b1", "1,2"))
        self.assertEqual(TelegramBotConfig.objects.get().admin_bot_id, "b2")

    def test_log_details_with_date_filter(self):
        LogDetails.objects.create(user_id=USER, index_name="nifty", log="old", time="1000")
        LogDetails.objects.create(user_id=USER, index_name="nifty", log="new", time="1793161214")
        everything = self.call(self.user, "get", "/get_log_details")["data"]
        self.assertEqual(len(everything), 2)
        recent = self.call(self.user, "post", "/get_log_details", {"start_date": "2026-01-01"})["data"]
        self.assertEqual([log["log"] for log in recent], ["new"])
        by_get = self.call(self.user, "get", "/get_log_details", {"end_date": "2000-01-01"})["data"]
        self.assertEqual([log["log"] for log in by_get], ["old"])
