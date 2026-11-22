"""Shared plumbing for views: auth, JSON body parsing, uniform responses and errors.

    @api(POST)                      logged-in user (session)
    @api(POST, auth=ADMIN)          staff user
    @api(POST, auth=TOKEN)          ?token=<key> webhook callers (TradingView etc.)
    @api(GET, auth=PUBLIC)          no auth

The view receives `request.email` and `request.json` (parsed body, {} if empty).
Errors never escape as 500s: bad JSON, validation errors and unexpected
exceptions all become a {"status": "failed", "message": ...} response.
"""
import json
from functools import wraps

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from plutusAI.server.authentication.authentication import QueryParamTokenAuthentication
from plutusAI.server.base import addLogDetails, admin_check, check_user_session
from plutusAI.server.constants import (  # GET/POST/PUT re-exported for views
    ERROR, FAILED, GET, GLOBAL_ERROR, POST, PUT, INVALID_JSON, LOGIN_URL, MESSAGE, STATUS, SUCCESS,
    TASK_STATUS, UNAUTHORISED,
)
from plutusAI.server.telegram_notifier import sendTradeAlert

PUBLIC, SESSION, ADMIN, TOKEN, ADMIN_TOKEN = "public", "session", "admin", "token", "admin_token"


def ok(message=None, task_status=None, **extra):
    body = {STATUS: SUCCESS}
    if message is not None:
        body[MESSAGE] = message
    if task_status is not None:
        body[TASK_STATUS] = task_status
    return JsonResponse({**body, **extra})


def fail(message, task_status=None, status=200, **extra):
    body = {STATUS: FAILED, MESSAGE: message}
    if task_status is not None:
        body[TASK_STATUS] = task_status
    return JsonResponse({**body, **extra}, status=status)


def _authorised(request, auth):
    if auth == PUBLIC:
        return True
    if auth in (ADMIN, ADMIN_TOKEN):
        return admin_check(request.user)
    return check_user_session(request)


def _parse_body(request):
    body = request.body
    return json.loads(body) if body else {}


def api(*methods, auth=SESSION, alert=None, expose_errors=False):
    """`alert=(title, action)` also sends a Telegram alert when the view fails.
    `expose_errors` returns the exception text instead of the generic error."""

    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if not _authorised(request, auth):
                return fail(UNAUTHORISED)
            request.email = getattr(request.user, "email", None)
            try:
                request.json = _parse_body(request) if request.method != "GET" else {}
                return view(request, *args, **kwargs)
            except json.JSONDecodeError:
                return fail(INVALID_JSON)
            except ValueError as e:  # input validation (validate_* helpers)
                return fail(str(e), status=400)
            except (ValidationError, IntegrityError) as e:
                return fail(str(e))
            except Exception as e:
                addLogDetails(ERROR, f"{request.email} :: {view.__name__} error: {e}")
                if alert:
                    title, action = alert
                    sendTradeAlert(title, request.email, str(e), getattr(request, "json", {}), action)
                return fail(str(e) if expose_errors else GLOBAL_ERROR)

        wrapper = csrf_exempt(wrapper)
        if auth in (TOKEN, ADMIN_TOKEN):
            wrapper = api_view(list(methods))(
                authentication_classes([QueryParamTokenAuthentication])(
                    permission_classes([IsAuthenticated])(wrapper)
                )
            )
        return csrf_exempt(require_http_methods(list(methods))(wrapper))

    return decorator


def page(template, admin=False):
    """GET-only HTML page; anonymous users go to the login page."""

    @require_http_methods(["GET"])
    def view(request):
        if not check_user_session(request):
            return redirect(LOGIN_URL)
        if admin and not admin_check(request.user):
            return render(request, "unauthorised.html")
        return render(request, template)

    return view
