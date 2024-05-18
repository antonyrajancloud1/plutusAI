from django.urls import path, re_path
from plutusAI.server.constants import *
from plutusAI.server.tester import testerCheck
from . import views
from django.urls import re_path as url
from django.conf import settings

from django.views.static import serve

urlpatterns = [
    url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    url(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path(HOME_URL, views.home, name=HOME_URL),
    path(LOGIN_URL, views.login_user, name=LOGIN_URL),
    path("", views.default, name=DEFAULT_PAGE_URL),
    path(LOGOUT_URL, views.logout_view, name=LOGOUT_URL),
    path(GET_CONFIG_VALUES, views.get_config_values, name=GET_CONFIG_VALUES),
    path(ADD_USER, views.add_user, name=ADD_USER),
    path(UPDATE_CONFIG_VALUES, views.update_config_values, name=UPDATE_CONFIG_VALUES),
    path(GET_BROKER_DETAILS, views.get_broker_details, name=GET_BROKER_DETAILS),
    path(ADD_BROKER_DETAILS, views.add_broker_details, name=ADD_BROKER_DETAILS),
    path(EDIT_BROKER_DETAILS, views.update_broker_details, name=EDIT_BROKER_DETAILS),
    path(GET_ORDER_BOOK_DETAILS,views.get_order_book_details,name=GET_ORDER_BOOK_DETAILS),
    path(START_INDEX, views.start_index, name=START_INDEX),
    path(STOP_INDEX, views.stop_index, name=STOP_INDEX),
    path(PLANS, views.get_plan_details, name=PLANS),
    path(EDIT_PLAN, views.edit_plan_details, name=EDIT_PLAN),
    path(START_WS, views.start_ws, name=START_WS),
    path(DASHBOARD, views.getDashboardDetails, name=DASHBOARD),
    path(STOP_WS, views.stop_ws, name=STOP_WS),

    path("terster", testerCheck, name="terster"),
]
