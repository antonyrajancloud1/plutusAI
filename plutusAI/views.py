from builtins import int

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from plutusAI.server.AngelOneApp import *
from plutusAI.server.broker.AngelOne.AngelOneAuth import AngelOneAuth
from plutusAI.server.priceAction.priceActionScalper import *
from .server.authentication.authentication import QueryParamTokenAuthentication
from .server.manualOrder import *
from .server.websocket.WebsocketAngelOne import WebsocketAngelOne

import subprocess

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
        # user_id = data.get(USER_ID)
        return add_user_and_populate_data(data)
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
        REQUIRED_FIELDS = [
            "user_id", "broker_name", "broker_user_id",
            "is_demo_trading_enabled", "broker_password", "broker_forex_server"
        ]
        if not check_user_session(request):
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

        data_json = json.loads(request.body)

        # Validate required fields
        missing_fields = [field for field in REQUIRED_FIELDS if field not in data_json]
        if missing_fields:
            return JsonResponse({STATUS: FAILED, MESSAGE: f"Missing fields: {', '.join(missing_fields)}"})

        # Set index_group using broker_name
        broker_name = data_json.get("broker_name")
        current_index = get_index_group_by_broker(AVAILABLE_BROKERS, broker_name)

        # Only use model fields from input
        model_fields = {f.name for f in BrokerDetails._meta.fields}
        filtered_data = {key: data_json[key] for key in data_json if key in model_fields}

        # Add required calculated fields
        filtered_data["index_group"] = current_index[0]
        filtered_data["token_status"] = "added"

        # Create the object
        BrokerDetails.objects.create(**filtered_data)

        return JsonResponse({STATUS: SUCCESS, MESSAGE: BROKER_DETAILS_ADDED})

    except json.JSONDecodeError:
        return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON})
    except (ValidationError, IntegrityError) as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: str(e)})
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
            # broker_user_id = data.get(BROKER_USER_ID)
            index_group=data.get(INDEX_GROUP)
            print(index_group)
            validate_char_fields(data)
            print(data)
            user_data = BrokerDetails.objects.filter(
                user_id=user_email,index_group=index_group
            )
            print(user_data)
            user_data.update(**data)
            updated_data = BrokerDetails.objects.filter(
                user_id=user_email,index_group=index_group
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
            user_data = OrderBook.objects.filter(user_id=user_email).order_by("-entry_time")
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
                updateIndexConfiguration(user_email=user_email, index=data.get(INDEX_NAME), data=STAGE_INITIATED)
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
            return JsonResponse({STATUS: FAILED, MESSAGE: "Socket running", TASK_STATUS: True})
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
        # if check_user_session(request):
        #     user_email = get_user_email(request)
        #     dashboard_data= {"all_data": getUserDashboardDetails(user_email, False),
        #                      "today_data": getUserDashboardDetails(user_email, True)}
        #     return JsonResponse({STATUS: SUCCESS, "dashboard":dashboard_data})
        # else:
        #     return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
        if check_user_session(request):
            return render(request, "dashboard.html")
        else:
            return redirect(LOGIN_URL)
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
                updateScalperDetails(user_email, data.get(INDEX_NAME), data=STAGE_INITIATED)
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
        return render(request, "manual.html")
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

@csrf_exempt
@require_http_methods([POST])
def reGenerateAccessToken(request):
    if check_user_session(request):
        user_email = get_user_email(request)
        AngelOneAuth(user_email)
        return JsonResponse({STATUS: SUCCESS, MESSAGE: TOKEN_GENERATED,TASK_STATUS:	True })
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@csrf_exempt
@require_http_methods([GET])
def checkBrokerTokenStatus(request):
    try:
        if check_user_session(request):
            user_email = get_user_email(request)
            broker = Broker(user_email, INDIAN_INDEX).BrokerObject
            profile_details = broker.checkProfile()
            if profile_details[MESSAGE]=="SUCCESS":
                return JsonResponse({STATUS: SUCCESS, MESSAGE: "token_is_valid",TASK_STATUS:	True })
            else:
                return JsonResponse({STATUS: FAILED, MESSAGE: profile_details["errorcode"], TASK_STATUS: False})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except Exception as e:
        addLogDetails(ERROR,str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: "token_is_invalid",TASK_STATUS: False})
@csrf_exempt
@require_http_methods([GET])
def getAllManualOrderDetails(request):
    if not check_user_session(request):
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

    user_email = get_user_email(request)
    index = request.GET.get("index_name")

    if index:
        user_manual_details = ManualOrders.objects.filter(user_id=user_email, index_name=index)
    else:
        user_manual_details = ManualOrders.objects.filter(user_id=user_email)

    user_manual_details = list(user_manual_details.values())

    if user_manual_details:
        return JsonResponse({STATUS: SUCCESS, MESSAGE: user_manual_details, TASK_STATUS: True})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: INDEX_NOT_FOUND if index else 'No orders found'})


@csrf_exempt
@require_http_methods([POST])
def placeBuyOrderManual(request):
    if check_user_session(request):
        try:
            user_email = get_user_email(request)
            signal_data = json.loads(request.body)
            index = signal_data[INDEX_NAME]
            # strategy = data.get(STRATEGY, "DefaultStrategy")
            if index:
                user_manual_details = ManualOrders.objects.filter(user_id=user_email, index_name=index)
                data = list(user_manual_details.values())[0]
            data = remove_spaces_from_json(data)
            triggerOrder(user_email, data, signal_data, BUY)
            return JsonResponse({STATUS: SUCCESS, MESSAGE: "Message Exists BUY"})
        except Exception as e:
            print(e)
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@csrf_exempt
@require_http_methods([POST])
def placeSellOrderManual(request):
    if check_user_session(request):
        user_email = get_user_email(request)
        signal_data = json.loads(request.body)
        index = signal_data[INDEX_NAME]
        # strategy = data.get(STRATEGY, "DefaultStrategy")
        if index:
            user_manual_details = ManualOrders.objects.filter(user_id=user_email, index_name=index)
            data = list(user_manual_details.values())[0]
        data = remove_spaces_from_json(data)
        triggerOrder(user_email, data, signal_data, SELL)
        return JsonResponse({STATUS: SUCCESS, MESSAGE: "Message Exists SELL"})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@csrf_exempt
@require_http_methods([POST])
def placeExitOrderManual(request):
    if check_user_session(request):
        user_email = get_user_email(request)
        data = json.loads(request.body)
        # index = data[INDEX_NAME]
        strategy = data.get(STRATEGY, "DefaultStrategy")
        exitOrderWebhook(strategy, data, user_email)
        return JsonResponse({STATUS: SUCCESS, MESSAGE: "Message Done"})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@login_required
@csrf_exempt
@require_http_methods([PUT])
def update_manual_order_values(request):
    try:
        if check_user_session(request):
            user_email = get_user_email(request)
            data = json.loads(request.body)
            data = remove_spaces_from_json(data)
            index_name = data.get(INDEX_NAME)

            validate_numeric_fields(data)
            validate_float_field(data)
            validate_levels(data)
            user_data = ManualOrders.objects.filter(
                user_id=user_email, index_name=index_name
            )
            user_data.update(**data)
            updated_data = ManualOrders.objects.filter(
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


@csrf_exempt
@require_http_methods([POST])
@api_view([POST])
@authentication_classes([QueryParamTokenAuthentication])
@permission_classes([IsAuthenticated])
def placeBuyOrderWebHook(request):

    if check_user_session(request):
        try:
            user_email = get_user_email(request)
            signal_data = json.loads(request.body)
            index=signal_data[INDEX_NAME]
            # strategy = signal_data.get(STRATEGY, "DefaultStrategy")
            if index:
                user_manual_details = ManualOrders.objects.filter(user_id=user_email, index_name=index)
                data = list(user_manual_details.values())[0]
            data = remove_spaces_from_json(data)
            submit_triggerOrder(user_email, data, signal_data, BUY)
            # triggerOrder(user_email, data, signal_data, BUY)
            return JsonResponse({STATUS: SUCCESS, MESSAGE: "Message Done"})
        except Exception as e:
            print(e)
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@csrf_exempt
@require_http_methods([POST])
@api_view([POST])
@authentication_classes([QueryParamTokenAuthentication])
@permission_classes([IsAuthenticated])
def modifyToMarketOrderWebHook(request):

    if check_user_session(request):
        try:
            user_email = get_user_email(request)
            data = json.loads(request.body)
            index=data[INDEX_NAME]
            strategy = data.get(STRATEGY, "DefaultStrategy")
            if index:
                user_manual_details = ManualOrders.objects.filter(user_id=user_email, index_name=index)
                data = list(user_manual_details.values())[0]
            data = remove_spaces_from_json(data)
            submit_modifyToMarketOrder(user_email, data, strategy, BUY)
            # modifyToMarketOrder(user_email, data, strategy, BUY)
            return JsonResponse({STATUS: SUCCESS, MESSAGE: "Modified"})
        except Exception as e:
            print(e)
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@csrf_exempt
@require_http_methods([POST])
@api_view([POST])
@authentication_classes([QueryParamTokenAuthentication])
@permission_classes([IsAuthenticated])
def placeSellOrderWebHook(request):
    #@authentication_classes([TokenAuthentication])
    if check_user_session(request):
        user_email = get_user_email(request)
        signal_data = json.loads(request.body)
        index = signal_data[INDEX_NAME]
        # strategy = data.get(STRATEGY, "DefaultStrategy")
        if index:
            user_manual_details = ManualOrders.objects.filter(user_id=user_email, index_name=index)
            data = list(user_manual_details.values())[0]
        data = remove_spaces_from_json(data)
        submit_triggerOrder(user_email, data, signal_data, SELL)
        # triggerOrder(user_email, data, signal_data, SELL)
        return JsonResponse({STATUS: SUCCESS, MESSAGE: "Message Done"})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})


@csrf_exempt
@require_http_methods([POST])
def getAuthToken(request):
    if check_user_session(request):
        user = User.objects.filter(username=request.user).first()
        if user is None:
            # Handle the case where the user doesn't exist
            return JsonResponse({'error': 'User not found'}, status=400)
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({STATUS: SUCCESS, MESSAGE: str(token.key)})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@csrf_exempt
@require_http_methods([POST])
def regenerateAuthToken(request):
    if check_user_session(request):
        user = User.objects.filter(username=request.user).first()
        if user is None:
            # Handle the case where the user doesn't exist
            return JsonResponse({'error': 'User not found'}, status=400)
        Token.objects.filter(user=user).delete()
        new_token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({STATUS: SUCCESS, MESSAGE: str(new_token.key)})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@require_http_methods([GET])
@csrf_exempt
def getIndexDetails(request):
    if admin_check(request.user):
        try:
            index_data= IndexDetails.objects.values_list('index_name', flat=True).distinct()
            index_data_list = list(index_data.values())
            return JsonResponse({STATUS: SUCCESS, MESSAGE: {"index_data":index_data_list}})
        except Exception as e:
            print(e)
            return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@require_http_methods([POST])
@csrf_exempt
def updateIndexExpiryDetails(request):
    if admin_check(request.user):
        try:
            updateExpiryDetails()
            return JsonResponse({STATUS: SUCCESS, MESSAGE: "Expiry details Updated",TASK_STATUS: True})
        except Exception as e:
            print(e)
            return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})


@csrf_exempt
@require_http_methods([POST])
@api_view([POST])
@authentication_classes([QueryParamTokenAuthentication])
@permission_classes([IsAuthenticated])
def placeExitOrderWebHook(request):
    #@authentication_classes([TokenAuthentication])
    if check_user_session(request):
        user_email = get_user_email(request)
        data = json.loads(request.body)
        # index = data[INDEX_NAME]
        strategy = data.get(STRATEGY, "DefaultStrategy")
        submit_exitOrderWebhook(strategy,data,user_email)
        # exitOrderWebhook(strategy,data,user_email)
        return JsonResponse({STATUS: SUCCESS, MESSAGE: "Message Exists SELL"})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@csrf_exempt
@require_http_methods(["POST"])
@api_view(["POST"])
@authentication_classes([QueryParamTokenAuthentication])
@permission_classes([IsAuthenticated])
def exitAllOrdersWebHook(request):
    try:
        if not admin_check(request.user):
            return JsonResponse({STATUS: FAILED, MESSAGE: "UNAUTHORISED"})

        open_orders = OrderBook.objects.filter(exit_price=None)
        if not open_orders.exists():
            return JsonResponse({STATUS: SUCCESS, MESSAGE: "No open orders to exit"})

        for order in open_orders:
            data = {
                "index_name": order.index_name,
                "strategy": order.strategy
            }
            exitOrderWebhook(order.strategy, data, order.user_id)

        return JsonResponse({STATUS: SUCCESS, MESSAGE: "done for the day"})

    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: "Internal server error"})



@require_http_methods([GET])
@csrf_exempt
def getStrategySummary(request):
    if check_user_session(request):
        try:
            user_email = get_user_email(request)
            user_data = getStrategySummaryUsingEmail(user_email)
            print(user_data)
            return JsonResponse({STATUS: SUCCESS, "summary":user_data,TASK_STATUS: True})
        except Exception as e:
            print(e)
            return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@csrf_exempt
@require_http_methods([GET])
def get_flash_values(request):
    # user_email='user1@gmail.com'
    if check_user_session(request):
        user_email = get_user_email(request)
        if "index_name" in request.GET:
            index = request.GET.get("index_name")
            user_data = FlashDetails.objects.filter(user_id=user_email, index_name=index)
            user_profiles_list = list(user_data.values())
            user_profiles_list = remove_data_from_list(user_profiles_list)
            if len(user_profiles_list) > 0:
                return JsonResponse(user_profiles_list[0])
            else:
                return JsonResponse({STATUS: FAILED, MESSAGE: INDEX_NOT_FOUND})
        else:
            user_data = FlashDetails.objects.filter(user_id=user_email)
            user_profiles_list = list(user_data.values())
            remove_data_from_list(user_profiles_list)
            # return JsonResponse({ALL_CONFIG_VALUES: user_profiles_list})
            return JsonResponse({STATUS: SUCCESS, MESSAGE: user_profiles_list, TASK_STATUS: True})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@login_required
@csrf_exempt
@require_http_methods([PUT])
def update_flash_values(request):
    try:
        if check_user_session(request):
            user_email = get_user_email(request)
            data = json.loads(request.body)
            data = remove_spaces_from_json(data)
            index_name = data.get(INDEX_NAME)

            validate_numeric_fields(data)
            validate_float_field(data)
            # validate_levels(data)
            user_data = FlashDetails.objects.filter(
                user_id=user_email, index_name=index_name
            )
            user_data.update(**data)
            updated_data = FlashDetails.objects.filter(
                user_id=user_email, index_name=index_name
            )
            updated_list = remove_data_from_list(list(updated_data.values()))[0]

            return JsonResponse(
                {STATUS: SUCCESS, MESSAGE: FLASH_VALUES_UPDATED, "data": updated_list}
            )
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except json.JSONDecodeError as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON})
    except ValueError as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: str(e)}, status=400)
    except Exception as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})

@csrf_exempt  # need to remove
@require_http_methods([POST])
def start_flash(request):
    try:
        if check_user_session(request):
            # checkSocketStatus()
            user_email = get_user_email(request)
            data = json.loads(request.body)
            index_name = data.get(INDEX_NAME).replace("_", " ").title().replace(" ", "")
            # strategy = data.get(STRATEGY)
            addLogDetails(INFO, "Flash started for user: " + str(user_email) + " for index :" + index_name)

            user_data = JobDetails.objects.filter(
                user_id=user_email, index_name=data.get(INDEX_NAME), strategy=STRATEGY_FLASH
            )
            if user_data.count() > 0:
                return JsonResponse({STATUS: FAILED, MESSAGE: f"{index_name} Flash running"})
            else:
                updateFlashConfiguration(user_email=user_email, index=data.get(INDEX_NAME), data=STAGE_INITIATED)
                start_flash_job.delay(user_email, data.get(INDEX_NAME))
                index_name = data.get(INDEX_NAME).replace("_", " ").title().replace(" ", "")
                return JsonResponse({STATUS: SUCCESS, MESSAGE: f"{index_name} flash started"})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})

@csrf_exempt  # need to remove
@require_http_methods([POST])
def stop_flash(request):
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


def is_celery_running():
    try:
        app_name = "plutus.celery"
        result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        lines = result.stdout.splitlines()

        for line in lines:
            if 'celery' in line and app_name in line:
                return True
        return False

    except Exception as e:
        print(f"Error checking Celery status: {e}")

@csrf_exempt  # need to remove
@require_http_methods([GET])
def check_celery_status(request):
    if not admin_check(request.user):
        return JsonResponse({STATUS: FAILED, MESSAGE: "UNAUTHORISED"})
    try:
        if is_celery_running():
            return JsonResponse({"celery_running": True, "details": "Celery is running."})
        else:
            return JsonResponse({"celery_running": False, "details": "Celery is NOT running."})
    except Exception as e:
        return JsonResponse({"celery_running": False, "error": str(e)}, status=500)

@csrf_exempt  # need to remove
@require_http_methods([POST])
def stop_celery(request):
    if not admin_check(request.user):
        return JsonResponse({STATUS: FAILED, MESSAGE: "UNAUTHORISED"})
    else:
        return JsonResponse(stopCelery(request))

def stopCelery(request):
    try:
        if is_celery_running():
            subprocess.run(["pkill", "-f", "celery -A plutus.celery"], check=True)
            return {"success": True, "message": "Celery stopped successfully.","task_status":True}
        else:
            return {"success": False, "message": "Celery is not running.","task_status":False}
    except subprocess.CalledProcessError as e:
        return {"success": False, "message": f"Failed to stop Celery: {e}"}

@csrf_exempt  # need to remove
@require_http_methods([POST])
def restart_celery(request):
    if not admin_check(request.user):
        return JsonResponse({STATUS: FAILED, MESSAGE: "UNAUTHORISED"})
    if is_celery_running():
        stop_result = stopCelery(request)
        if not stop_result["success"]:
            return JsonResponse({"success": False, "message": "Failed to stop Celery. Restart aborted."})

        time.sleep(2)

    try:
        command = "celery -A plutus.celery worker --loglevel=info --autoscale=100,3"
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return JsonResponse({"success": True, "message": "Celery restarted successfully." ,"task_status":True})
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Failed to restart Celery: {e}"})

@csrf_exempt
@require_http_methods([GET])
def getOpenOrders(request):
    if check_user_session(request):
        user_email = get_user_email(request)
        # data = json.loads(request.body)
        broker = Broker(user_email, INDIAN_INDEX).BrokerObject

        return getOpenOrdersUsingEmail(user_email,broker)
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@csrf_exempt
@require_http_methods([POST])
@api_view([POST])
@authentication_classes([QueryParamTokenAuthentication])
@permission_classes([IsAuthenticated])
def placeForexBuy(request):
    if check_user_session(request):
        user_email = get_user_email(request)
        data_json = json.loads(request.body)
        broker = Broker(user_email, FOREX_INDEX).BrokerObject
        broker.placeOrderForex(0,data_json)
        return JsonResponse({STATUS: SUCCESS, MESSAGE: "Buy Completed"})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})
@csrf_exempt
@require_http_methods([POST])
@api_view([POST])
@authentication_classes([QueryParamTokenAuthentication])
@permission_classes([IsAuthenticated])
def placeForexSell(request):
    if check_user_session(request):
        user_email = get_user_email(request)
        data_json = json.loads(request.body)
        broker = Broker(user_email, FOREX_INDEX).BrokerObject
        broker_response = broker.placeOrderForex(1,data_json)
        return JsonResponse({STATUS: SUCCESS, MESSAGE: broker_response})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@csrf_exempt
@require_http_methods([POST])
@api_view([POST])
@authentication_classes([QueryParamTokenAuthentication])
@permission_classes([IsAuthenticated])
def closeForexSell(request):
    if check_user_session(request):
        user_email = get_user_email(request)
        data_json = json.loads(request.body)
        broker = Broker(user_email, FOREX_INDEX).BrokerObject
        broker_response = broker.exitOrderForex(data_json)
        return JsonResponse({STATUS: SUCCESS, MESSAGE: broker_response})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

def safe_json_body(request):
    """Helper to safely parse JSON body from request"""
    try:
        if request.body:
            return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        pass
    return {}
@csrf_exempt
@require_http_methods([GET])
def getStrategyDetails(request):
    if check_user_session(request):
        user_email = get_user_email(request)
        data = safe_json_body(request)
        index_name = data.get(INDEX_NAME)
        user_strategy_details = ManualOrders.objects.filter(user_id=user_email)
        if index_name:
            user_strategy_details = user_strategy_details.filter(index_name=index_name)
        strategy_details = list(user_strategy_details.values())
        print(strategy_details)

        return JsonResponse({STATUS: SUCCESS, "data": strategy_details})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})





@csrf_exempt
@require_http_methods([PUT])
def updateStrategy(request):
    if check_user_session(request):
        user_email = get_user_email(request)
        data = safe_json_body(request)

        strategy_name = data.get("strategy_name")
        update_fields = data.get("fields", {})  # {field: value}

        if not strategy_name or not update_fields:
            return JsonResponse({STATUS: FAILED, MESSAGE: "Invalid request"})

        try:
            updated = ManualOrders.objects.filter(user_id=user_email, strategy_name=strategy_name).update(**update_fields)
            if updated:
                return JsonResponse({STATUS: SUCCESS, MESSAGE: "Updated successfully"})
            else:
                return JsonResponse({STATUS: FAILED, MESSAGE: "No record found"})
        except Exception as e:
            return JsonResponse({STATUS: FAILED, MESSAGE: str(e)})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@csrf_exempt
@require_http_methods([POST])
def deleteStrategy(request):
    if check_user_session(request):
        user_email = get_user_email(request)
        data = safe_json_body(request)

        strategy_name = data.get("strategy_name")

        if not strategy_name:
            return JsonResponse({STATUS: FAILED, MESSAGE: "Strategy name required"})

        try:
            deleted, _ = ManualOrders.objects.filter(user_id=user_email, strategy_name=strategy_name).delete()
            if deleted:
                return JsonResponse({STATUS: SUCCESS, MESSAGE: "Deleted successfully"})
            else:
                return JsonResponse({STATUS: FAILED, MESSAGE: "No record found"})
        except Exception as e:
            return JsonResponse({STATUS: FAILED, MESSAGE: str(e)})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})

@csrf_exempt
@require_http_methods([POST])
def addStrategy(request):
    if check_user_session(request):
        user_email = get_user_email(request)
        data = safe_json_body(request)
        strategy_name = data.get("strategy_name")
        index_name = data.get("index_name")
        if not strategy_name or not index_name:
            return JsonResponse({STATUS: FAILED, "MESSAGE": "strategy_name and index_name are mandatory"})

        # Check if strategy already exists for this user
        if ManualOrders.objects.filter(user_id=user_email, strategy_name=strategy_name).exists():
            return JsonResponse({STATUS: FAILED, "MESSAGE": f"Strategy '{strategy_name}' already exists"})

        try:
            strategy = ManualOrders.objects.create(
                user_id=user_email,
                strategy_name=data.get("strategy_name"),
                index_name=data.get("index_name"),
                strike=data.get("strike"),
                lots=data.get("lots"),
                on_candle_close=data.get("on_candle_close", False),
                producttype=data.get("producttype", "INTRADAY"),
                timeframe=data.get("timeframe", "FIVE_MINUTE"),
                index_group=data.get("index_group", "indian_index"),
                strategy_type="custom"
            )

            return JsonResponse({STATUS: SUCCESS, "message": "Strategy added", "strategy_name": strategy.strategy_name})
        except Exception as e:
            return JsonResponse({STATUS: FAILED, MESSAGE: str(e)})
    else:
        return JsonResponse({STATUS: FAILED, MESSAGE: UNAUTHORISED})