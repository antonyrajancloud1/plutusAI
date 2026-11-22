"""Records every route's response for anonymous / user / admin callers.

Used to compare behaviour before and after refactoring views:
    DJANGO_SETTINGS_MODULE=plutus.settings_test python -m plutusAI.testing.route_snapshot out.json
All external side effects (broker, Celery, subprocess, Telegram, websockets) are stubbed.
"""
import json
import logging
import sys
from unittest import mock

import django

SKIP = {"media/", "static/", "test"}
BODIES = {
    "none": None,
    "index": {"index_name": "nifty", "strategy": "ST_target", "ws_type": "1"},
}


def snapshot():
    from django.contrib.auth.models import User
    from django.test import Client
    from django.test.utils import setup_test_environment
    from rest_framework.authtoken.models import Token

    from plutusAI.models import IndexDetails, ManualOrders
    from plutusAI.testing.fakes import BrokerFactory, FakeBroker

    setup_test_environment()
    logging.disable(logging.CRITICAL)
    from django.db import connection
    from django.test.utils import setup_databases

    setup_databases(verbosity=0, interactive=False)

    user = User.objects.create_user("u", "u@test.in", "pw")
    admin = User.objects.create_user("a", "a@test.in", "pw", is_staff=True)
    tokens = {"user": Token.objects.create(user=user).key, "admin": Token.objects.create(user=admin).key}
    IndexDetails.objects.create(index_name="nifty", index_token="1", ltp="0", last_updated_time="0",
                                qty="65", current_expiry="03-Nov-2026", next_expiry="09-Nov-2026")
    for email in ("u@test.in", "a@test.in"):
        ManualOrders.objects.create(user_id=email, index_name="nifty", strike="100", lots="1",
                                    strategy_name="ST_target")

    fake = BrokerFactory(FakeBroker(demo=True))
    stub = mock.MagicMock()
    patches = [
        mock.patch("subprocess.run", stub), mock.patch("subprocess.Popen", stub),
        mock.patch("celery.app.task.Task.delay", stub),
        mock.patch("celery.app.task.Task.apply_async", stub),
        mock.patch("requests.post", stub), mock.patch("requests.get", stub),
        mock.patch("time.sleep", lambda *_: None),
    ]
    for module in ("plutusAI.views", "plutusAI.views.admin", "plutusAI.views.orders",
                   "plutusAI.server.manualOrder", "plutusAI.server.base"):
        for name in ("Broker", "AngelOneAuth", "WebsocketAngelOne", "submit_triggerOrder",
                     "submit_exitOrderWebhook", "submit_modifyToMarketOrder"):
            target = f"{module}.{name}"
            try:
                __import__(module, fromlist=[name]).__dict__[name]
            except (KeyError, ImportError):
                continue
            patches.append(mock.patch(target, fake if name == "Broker" else stub))
    for p in patches:
        p.start()

    from plutusAI import urls

    routes = sorted({str(p.pattern) for p in urls.urlpatterns} - SKIP)
    routes = [r for r in routes if not r.startswith("^")]
    results = {}
    for who in ("anon", "user", "admin"):
        client = Client()
        for route in routes:
            for method in ("get", "post", "put"):
                for body_name, body in BODIES.items():
                    if who != "anon":  # re-login: /logout would end the session
                        client.force_login(user if who == "user" else admin)
                    url = "/" + route
                    if who != "anon":
                        url += f"?token={tokens[who]}"
                    try:
                        if method == "get":  # GET sends the fields as query params
                            kwargs = {"data": body or {}}
                        else:
                            kwargs = {"content_type": "application/json"}
                            if body is not None:
                                kwargs["data"] = json.dumps(body)
                        resp = getattr(client, method)(url, **kwargs)
                        if resp.status_code in (301, 302):
                            out = f"redirect:{resp.get('Location', '').split('?')[0]}"
                        elif resp.get("Content-Type", "").startswith("application/json"):
                            out = json.loads(resp.content)
                        else:
                            out = "html"
                        results[f"{who} {method.upper()} /{route} [{body_name}]"] = [resp.status_code, out]
                    except Exception as e:
                        results[f"{who} {method.upper()} /{route} [{body_name}]"] = ["EXC", type(e).__name__]
    return results


if __name__ == "__main__":
    django.setup()
    data = snapshot()
    with open(sys.argv[1], "w") as f:
        json.dump(data, f, indent=1, sort_keys=True, default=str)
    print(f"{len(data)} responses recorded -> {sys.argv[1]}")
