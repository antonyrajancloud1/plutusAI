import json
from builtins import int

from django import forms
from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from plutusAI.server.AngelOneApp import *
from plutusAI.server.base import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.db.models import Q

from plutusAI.server.constants import *
from plutusAI.server.priceAction.priceActionScalper import *
from .models import *
from datetime import datetime, timedelta

from .server.broker.Broker import Broker
from .server.websocket.WebsocketAngelOne import WebsocketAngelOne


def invaid_url(request, exception):
    return render(request, "invaid_url.html", status=404)


def internal_error(request):
    return render(request, "internal_error.html", status=500)


@require_http_methods([GET])
def default(request):
    if check_user_session(request):
        return redirect(HOME_URL)
    else:
        return redirect(LOGIN_URL)


@require_http_methods([GET])
def home(request):
    if check_user_session(request):
        return render(request, HOME_PAGE_URL)
    else:
        return redirect(LOGIN_URL)


# @require_http_methods([POST])
@csrf_exempt
def login_user(request):
    if check_user_session(request):
        return redirect(HOME_URL)
    elif request.method == POST:
        username = request.POST[USER_NAME]
        password = request.POST[PASSWORD]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({STATUS: SUCCESS, MESSAGE: LOGIN_SUCCESS})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: LOGIN_ERROR})
    else:
        return render(request, LOGIN_PAGE_URL)


@require_http_methods([GET])
def logout_view(request):
    try:
        if check_user_session(request):
            logout(request)
            return JsonResponse({STATUS: SUCCESS, MESSAGE: LOGOUT_SUCCESS})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except Exception as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: LOGOUT_ERROR})


@csrf_exempt
@require_http_methods([GET])
def get_config_values(request):
    # user_email='user1@gmail.com'
    if check_user_session(request):
        user_email = get_user_email(request)
        if "index_name" in request.GET:
            index = request.GET.get("index_name")
            user_profiles_list = getIndexConfiguration(user_email, index)
            if len(user_profiles_list) > 0:
                return JsonResponse(user_profiles_list)
            else:
                return JsonResponse({STATUS: FAILED, MESSAGE: INDEX_NOT_FOUND})
        else:
            user_data = Configuration.objects.filter(user_id=user_email)
            user_profiles_list = list(user_data.values())
            remove_data_from_list(user_profiles_list)
            return JsonResponse({ALL_CONFIG_VALUES: user_profiles_list})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})


@require_http_methods([POST])
@csrf_exempt
def add_user(request):
    if admin_check(request.user):
        data = json.loads(request.body)
        user_id = data.get(USER_ID)
        return add_user_and_populate_data(user_id)
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})


@login_required
@csrf_exempt
@require_http_methods([PUT])
def update_config_values(request):
    try:
        if check_user_session(request):
            user_email = get_user_email(request)
            data = json.loads(request.body)
            data = remove_spaces_from_json(data)
            index_name = data.get(INDEX_NAME)

            validate_numeric_fields(data)
            validate_float_field(data)
            validate_levels(data)
            user_data = Configuration.objects.filter(
                user_id=user_email, index_name=index_name
            )
            user_data.update(**data)
            updated_data = Configuration.objects.filter(
                user_id=user_email, index_name=index_name
            )
            updated_list = remove_data_from_list(list(updated_data.values()))[0]

            return JsonResponse(
                {STATUS: SUCCESS, MESSAGE: CONFIG_VALUES_UPDATED, "data": updated_list}
            )
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except json.JSONDecodeError as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON})
    except ValueError as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: str(e)}, status=400)
    except Exception as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


@login_required
@require_http_methods([GET])
@csrf_exempt
def get_broker_details(request):
    try:
        if check_user_session(request):
            user_email = get_user_email(request)
            if "broker_name" in request.GET:
                broker_name = request.GET.get("broker_name")
                return get_broker_details_using_id_and_group(user_email, broker_name)
            else:
                return get_broker_details_using_id(user_email)
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


# @login_required
@require_http_methods([POST])
@csrf_exempt  # need to remove
def add_broker_details(request):
    try:
        if check_user_session(request):
            data_json = json.loads(request.body)
            user_email = get_user_email(request)
            broker_name = data_json.get(BROKER_NAME)
            current_index = get_index_group_by_broker(AVAILABLE_BROKERS, broker_name)
            BrokerDetails.objects.create(
                user_id=user_email,
                broker_user_id=data_json.get(BROKER_USER_ID),
                broker_user_name=data_json.get(BROKER_USER_NAME),
                broker_mpin=data_json.get(BROKER_MPIN),
                broker_api_token=data_json.get(BROKER_API_TOKEN),
                broker_qr=data_json.get(BROKER_QR),
                broker_name=data_json.get(BROKER_NAME),
                is_demo_trading_enabled=data_json.get(IS_DEMO_TRADING_ENABLED),
                token_status="added",
                index_group=current_index[0],
            )
            return JsonResponse({STATUS: SUCCESS, MESSAGE: BROKER_DETAILS_ADDED})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except json.JSONDecodeError as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


# @login_required
@csrf_exempt  # need to remove
@require_http_methods([PUT])
def update_broker_details(request):
    try:
        if check_user_session(request):
            user_email = get_user_email(request)
            data = json.loads(request.body)
            broker_user_id = data.get(BROKER_USER_ID)
            validate_char_fields(data)
            user_data = BrokerDetails.objects.filter(
                user_id=user_email
            )
            user_data.update(**data)
            updated_data = BrokerDetails.objects.filter(
                user_id=user_email
            )
            updated_list = list(updated_data.values())
            for data in updated_list:
                data.pop(ID)
            return JsonResponse({STATUS: SUCCESS, MESSAGE: BROKER_DETAILS_UPDATED})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except json.JSONDecodeError as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON}, status=400)
    except ValueError as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: str(e)})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


# @login_required
@require_http_methods([GET])
@csrf_exempt  # need to remove
def get_order_book_details(request):
    try:
        if check_user_session(request):
            # sample_data={"user_id":"antonyasp12@gmail.com","script_name":"NIFTY21000CE","qty":"100","entry_price":"150","exit_price":"250","status":"order_exited"}
            # add_order_book_details(sample_data)
            user_email = get_user_email(request)
            user_data = OrderBook.objects.filter(user_id=user_email)
            order_book_list = list(user_data.values())
            for data in order_book_list:
                data.pop(ID)
                if data[EXIT_PRICE] == None:
                    data[EXIT_PRICE] = ""
                if data[EXIT_TIME] == None:
                    data[EXIT_TIME] = ""
            return JsonResponse({ORDER_BOOK_DETAILS: order_book_list})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except json.JSONDecodeError as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


def add_order_book_details(data_json):
    try:
        current_time = getCurrentTimestamp()
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        OrderBook.objects.create(
            user_id=data_json.get(USER_ID),
            script_name=data_json.get(SCRIPT_NAME),
            qty=data_json.get(QTY),
            entry_price=data_json.get(ENTRY_PRICE),
            exit_price=data_json.get(EXIT_PRICE),
            status=data_json.get(STATUS),

        )
        #time=current_time_str,
    except json.JSONDecodeError as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


@csrf_exempt  # need to remove
@require_http_methods([POST])
def start_index(request):
    try:
        if check_user_session(request):
            # checkSocketStatus()
            user_email = get_user_email(request)
            # user_email='user1@gmail.com'
            data = json.loads(request.body)
            index_name = data.get(INDEX_NAME).replace("_", " ").title().replace(" ", "")
            strategy = data.get(STRATEGY)
            addLogDetails(INFO, "Hunter started for user: " + str(user_email) + " for index :" + index_name)

            user_data = JobDetails.objects.filter(
                user_id=user_email, index_name=data.get(INDEX_NAME), strategy=STRATEGY_HUNTER
            )
            if user_data.count() > 0:
                return JsonResponse({STATUS: FAILED, MESSAGE: f"{index_name} process running"})
            else:
                start_index_job.delay(user_email, data.get(INDEX_NAME))
                index_name = data.get(INDEX_NAME).replace("_", " ").title().replace(" ", "")
                return JsonResponse({STATUS: SUCCESS, MESSAGE: f"{index_name} started"})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


@csrf_exempt  # need to remove
@require_http_methods([POST])
def stop_index(request):
    try:
        if check_user_session(request):
            # raw_text = request.body.decode('utf-8')
            user_email = get_user_email(request)
            # user_email='user1@gmail.com'
            data = json.loads(request.body)
            return terminate_task(user_email, data.get(INDEX_NAME), data.get(STRATEGY))
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


@require_http_methods([GET])
def get_plan_details(request):
    try:
        if check_user_session(request):
            user_email = get_user_email(request)
            user_data = PaymentDetails.objects.filter(user_id=user_email)
            user_data = list(user_data.values())
            user_data = remove_data_from_list(user_data)
            return JsonResponse({PLAN_DETAILS: user_data})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


@require_http_methods([PUT])
@csrf_exempt
def edit_plan_details(request):
    try:
        if admin_check(request.user):
            data_json = json.loads(request.body)
            user_email = data_json.get("user_id")

            current_time = datetime.now()
            renew_date = current_time + timedelta(days=int(data_json.get("renew_date")))
            renew_date = renew_date.strftime("%Y-%m-%d %H:%M:%S")
            data_json["renew_date"] = renew_date
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            user_data = PaymentDetails.objects.filter(user_id=user_email)
            if user_data.count() > 0:
                user_data.update(**data_json)
            else:
                PaymentDetails.objects.create(
                    user_id=user_email,
                    registed_date=current_time_str,
                    renew_date=renew_date,
                    opted_index=data_json.get("opted_index"),
                )
            return JsonResponse({STATUS: SUCCESS, MESSAGE: data_json})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except json.JSONDecodeError as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


@require_http_methods([POST])
@csrf_exempt
def start_ws(request):
    if admin_check(request.user):
        data_json = json.loads(request.body)
        ws_type = str(data_json.get("ws_type"))
        user_data = None
        if ws_type == "1":
            user_data = JobDetails.objects.filter(
                user_id=ADMIN_USER_ID, index_name=SOCKET_JOB, strategy=SOCKET_JOB
            )
        elif ws_type == "2" or ws_type == "3":
            user_data = JobDetails.objects.filter(
                user_id=ADMIN_USER_ID, index_name=HTTP_JOB, strategy=HTTP_JOB
            )
        if user_data.count() > 0:
            return JsonResponse({STATUS: FAILED, MESSAGE: "Socket running", "task_status": True})
        else:
            return start_ws_job(ws_type)
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})


@require_http_methods([POST])
@csrf_exempt
def stop_ws(request):
    try:
        if admin_check(request.user):
            data_json = json.loads(request.body)
            ws_type = str(data_json.get("ws_type"))
            if ws_type == "1":
                return terminate_task(ADMIN_USER_ID, SOCKET_JOB, SOCKET_JOB)
            elif ws_type == "2" or ws_type == "3":
                return terminate_task(ADMIN_USER_ID, HTTP_JOB, HTTP_JOB)
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


# def start_ws_job(ws_type):
#     try:
#         updateExpiryDetails.delay()
#         if ws_type is None or ws_type.__eq__("1"):
#             createV1Socket.delay()
#         elif ws_type.__eq__("2"):
#             createAngleOne.delay()
#         elif ws_type.__eq__("3"):
#             createHttpData.delay()
#         return JsonResponse({STATUS: SUCCESS, MESSAGE: "WS started"})
#     except json.JSONDecodeError as e:
#         return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON})
#     except Exception as e:
#         addLogDetails(ERROR, str(e))
#         return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})

# index_data = IndexDetails.objects.filter(index_token=token)
# index_data.update(**data)


@require_http_methods([GET])
def getDashboardDetails(request):
    try:
        if check_user_session(request):
            user_email = get_user_email(request)
            start_of_day_timestamp = int(
                time.mktime(time.strptime(time.strftime("%Y-%m-%d 00:00:00"), "%Y-%m-%d %H:%M:%S")))
            ob_data = OrderBook.objects.filter(user_id=user_email, exit_time__gte=start_of_day_timestamp)
            ob_data = list(ob_data.values())
            total = 0
            for data in ob_data:
                total += float(data[TOTAL])
            return JsonResponse({STATUS: SUCCESS, "data": {TOTAL: total}})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


# def checkSocketStatus():
#     user_data = JobDetails.objects.filter(
#         user_id=ADMIN_USER_ID, index_name=SOCKET_JOB
#     )
#     if user_data.count() > 0:
#         return JsonResponse({STATUS: FAILED, MESSAGE: "Socket running"})
#     else:
#         start_ws_job(SOCKET_JOB_TYPE)
#         return JsonResponse({STATUS: SUCCESS, MESSAGE: "Socket Job started"})

@csrf_exempt
@require_http_methods([POST])
def start_scalper(request):
    print("into start_scalper")

    try:
        #
        if check_user_session(request):
            #         #checkSocketStatus()
            user_email = get_user_email(request)
            data = json.loads(request.body)
            index_name = data.get(INDEX_NAME).replace("_", " ").title().replace(" ", "")
            addLogDetails(INFO, "scalper started for user: " + str(user_email) + " for index :" + index_name)
            user_data = JobDetails.objects.filter(
                user_id=user_email, index_name=data.get(INDEX_NAME), strategy=SCALPER
            )
            if user_data.count() > 0:
                return JsonResponse({STATUS: FAILED, MESSAGE: f"{index_name} scalper running"})
            else:
                start_scalper_task.delay(user_email, data.get(INDEX_NAME))
                index_name = data.get(INDEX_NAME).replace("_", " ").title().replace(" ", "")
                return JsonResponse({STATUS: SUCCESS, MESSAGE: f"{index_name} scalper started"})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


@require_http_methods([GET])
def html_test(request):
    if check_user_session(request):
        return render(request, "testHtml.html")
    else:
        return redirect(LOGIN_URL)


@login_required
@csrf_exempt
@require_http_methods([PUT])
def update_scalper_values(request):
    try:
        if check_user_session(request):
            user_email = get_user_email(request)
            data = json.loads(request.body)
            data = remove_spaces_from_json(data)
            index_name = data.get(INDEX_NAME)

            validate_numeric_fields(data)
            validate_float_field(data)
            # validate_levels(data)
            user_data = ScalperDetails.objects.filter(
                user_id=user_email, index_name=index_name
            )
            user_data.update(**data)
            updated_data = ScalperDetails.objects.filter(
                user_id=user_email, index_name=index_name
            )
            updated_list = remove_data_from_list(list(updated_data.values()))[0]

            return JsonResponse(
                {STATUS: SUCCESS, MESSAGE: SCALPER_VALUES_UPDATED, "data": updated_list}
            )
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except json.JSONDecodeError as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON})
    except ValueError as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: str(e)}, status=400)
    except Exception as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


@csrf_exempt
@require_http_methods([GET])
def get_scalper_values(request):
    # user_email='user1@gmail.com'
    if check_user_session(request):
        user_email = get_user_email(request)
        if "index_name" in request.GET:
            index = request.GET.get("index_name")
            user_data = ScalperDetails.objects.filter(user_id=user_email, index_name=index)
            user_profiles_list = list(user_data.values())
            user_profiles_list = remove_data_from_list(user_profiles_list)
            if len(user_profiles_list) > 0:
                return JsonResponse(user_profiles_list[0])
            else:
                return JsonResponse({STATUS: FAILED, MESSAGE: INDEX_NOT_FOUND})
        else:
            user_data = ScalperDetails.objects.filter(user_id=user_email)
            user_profiles_list = list(user_data.values())
            remove_data_from_list(user_profiles_list)
            return JsonResponse({ALL_CONFIG_VALUES: user_profiles_list})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})


@require_http_methods([GET])
def admin_console(request):
    if check_user_session(request):
        if admin_check(request.user):
            return render(request, "admin_console.html")
        else:
            return render(request, "unauthorised.html")
    else:
        return redirect(LOGIN_URL)


@csrf_exempt
@require_http_methods([GET])
def check_task_status(request):
    try:
        if admin_check(request.user):
            socket_data = JobDetails.objects.filter(
                user_id=ADMIN_USER_ID, index_name=SOCKET_JOB, strategy=SOCKET_JOB
            )
            socket_data = list(socket_data.values())
            print(socket_data)

            if len(socket_data) > 0:
                result = AsyncResult(socket_data[0]["job_id"])

                status_str = str(result.status)
                print(status_str)
                if status_str == 'PENDING':
                    return JsonResponse({STATUS: SUCCESS, MESSAGE: "Socket running", "task_status": True})
                else:
                    return JsonResponse({STATUS: FAILED, MESSAGE: "Socket not running", "task_status": False})
            else:
                return JsonResponse({STATUS: SUCCESS, MESSAGE: "No Socket Job Present", "task_status": False})
        else:
            return render(request, "unauthorised.html")
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


@csrf_exempt
@require_http_methods([POST])
def buy_manual_order(request):
    print("buy_manual_order")

    try:
        #
        if check_user_session(request):
            user_email = get_user_email(request)
            data = json.loads(request.body)
            index_name = data["index_name"]
            user_orders = OrderBook.objects.filter(user_id=user_email, strategy=STRATEGY_MANUAL, index_name=index_name)
            user_manual_details = ManualOrders.objects.filter(user_id=user_email, index_name=index_name)

            index_data = IndexDetails.objects.filter(index_name=index_name)
            index_data = list(index_data.values())[0]

            user_manual_details = list(user_manual_details.values())[0]
            strike = user_manual_details[STRIKE]
            user_qty = int(user_manual_details[LOTS]) * int(index_data[QTY])
            print(user_orders)
            broker_data = get_broker_details_json_using_id(user_email)[0]
            print(broker_data)
            if list(user_orders.values()).__len__() > 0:
                print("ORDER_PRESENT")
                return JsonResponse({STATUS: FAILED, MESSAGE: ORDER_PRESENT})
            else:
                print("ORDER_NOT_PRESENT")
                BrokerObject = Broker(user_email, broker_data[INDEX_GROUP]).BrokerObject
                is_demo_enabled = BrokerObject.is_demo_enabled
                print(is_demo_enabled)
                currentPremiumPlaced = getTradingSymbol(index_name) + str(
                    BrokerObject.getCurrentAtm(index_name) - int(strike)) + "CE"
                optionDetails = BrokerObject.getCurrentPremiumDetails(NFO, currentPremiumPlaced)
                if is_demo_enabled:
                    print("Place dummy order")
                    optionBuyPrice = BrokerObject.getLtpForPremium(optionDetails)
                    data = {USER_ID: user_email, SCRIPT_NAME: currentPremiumPlaced, QTY: user_qty,
                            ENTRY_PRICE: optionBuyPrice, STATUS: ORDER_PLACED, STRATEGY: STRATEGY_MANUAL,
                            INDEX_NAME: index_name}
                    print(data)
                    addOrderBookDetails(data, True)
                else:
                    print("Place Broker order")
                    BrokerObject.placeOrder()

                symbol_token = BrokerObject.getTokenForSymbol(currentPremiumPlaced)
                angle_candle = WebsocketAngelOne(user_email,index_name,symbol_token,STRATEGY_MANUAL)
                angle_candle.connectWS()
                return JsonResponse({STATUS: SUCCESS, MESSAGE: ORDER_PLACED})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})
