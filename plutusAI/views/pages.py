"""HTML pages, login and logout."""
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from plutusAI.server.api import api, fail, ok, page
from plutusAI.server.base import check_user_session
from plutusAI.server.constants import (
    DASHBOARD, GET, LOGIN_ERROR, LOGIN_PAGE_URL, LOGIN_SUCCESS,
    LOGIN_URL, LOGOUT_SUCCESS, PASSWORD, POST, USER_NAME,
)

# /dashboard is the only UI. The old page URLs still work (bookmarks) and open
# the matching section of it.
getDashboardDetails = page("dashboard.html")


def _dashboard_section(section):
    @require_http_methods([GET])
    def view(request):
        if not check_user_session(request):
            return redirect(LOGIN_URL)
        return redirect(f"{reverse(DASHBOARD)}#/{section}")

    return view


home = _dashboard_section("dashboard")
html_test = _dashboard_section("manual")
viewLogDetails = _dashboard_section("logs")
admin_console = _dashboard_section("admin")


def invaid_url(request, exception):
    return render(request, "invaid_url.html", status=404)


def internal_error(request):
    return render(request, "internal_error.html", status=500)


@require_http_methods([GET])
def default(request):
    return redirect(DASHBOARD if check_user_session(request) else LOGIN_URL)


@csrf_exempt
def login_user(request):
    if check_user_session(request):
        return redirect(DASHBOARD)
    if request.method != POST:
        return render(request, LOGIN_PAGE_URL)
    user = authenticate(
        request,
        username=request.POST.get(USER_NAME),
        password=request.POST.get(PASSWORD),
    )
    if user is None:
        return fail(LOGIN_ERROR)
    login(request, user)
    return ok(LOGIN_SUCCESS)


@api(GET)
def logout_view(request):
    logout(request)
    return ok(LOGOUT_SUCCESS)
