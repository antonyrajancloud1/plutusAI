from datetime import datetime, timedelta
import json
import logging
import os
import re
import time
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
import pandas as pd
import requests
from plutusAI.models import *
from plutusAI.server.constants import *
import pytz
from dateutil.rrule import rrule, WEEKLY, TH, TU, WE, MO
from celery import shared_task
from celery.result import AsyncResult


def admin_check(user):
    return user.is_authenticated and user.is_staff


def check_user_session(request):
    return request.user.is_authenticated


def get_user_email(request):
    email = request.user.email
    return email


def add_user(username, email, password):
    if User.objects.filter(username=username).exists():
        return JsonResponse({STATUS: SUCCESS, MESSAGE: USER_EXISTS})
    else:
        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        user.first_name = str(username)
        user.save()

        return JsonResponse({STATUS: SUCCESS, MESSAGE: USER_ADDED})


def add_config_values(data_json):
    Configuration.objects.create(
        index_name=data_json.get(INDEX_NAME),
        initial_sl=data_json.get(INITIAL_SL),
        is_place_sl_required=data_json.get(IS_SL_REQUIRED),
        safe_sl=data_json.get(SAFE_SL),
        target_for_safe_sl=data_json.get(TARGET_FOR_SAFE_SL),
        trailing_points=data_json.get(TRAILING_POINTS),
        trend_check_points=data_json.get(TREND_CHECK_POINTS),
        levels=data_json.get(LEVELS),
        user_id=data_json.get(USER_ID),
        start_scheduler=data_json.get(START_SCHEDULER),
        lots=data_json.get(LOTS),
    )


def addAllIndexValues(user_id):
    nifty_default_values = NIFTY_DEFAULT_VALUES
    bank_nifty_default_values = BANK_NIFTY_DEFAULT_VALUES
    finnifty_default_values = FINNIFTY_DEFAULT_VALUES
    nifty_default_values[USER_ID] = user_id
    bank_nifty_default_values[USER_ID] = user_id
    finnifty_default_values[USER_ID] = user_id
    index_values = []
    index_values.append(nifty_default_values)
    index_values.append(bank_nifty_default_values)
    index_values.append(finnifty_default_values)

    for value in index_values:
        add_config_values(value)


def add_user_and_populate_data(user_id):
    try:
        username = str(user_id).split("@")[0]
        password = "New@2024"
        user_details = add_user(username, user_id, password)
        user_response = json.loads(user_details.content)
        addLogDetails(INFO, "New user added Response:" + str(user_response))
        if user_response.get(MESSAGE).__eq__(USER_ADDED):
            addAllIndexValues(user_id)
            return JsonResponse(
                {
                    STATUS: SUCCESS,
                    MESSAGE: "User added",
                    USER_NAME: username,
                    PASSWORD: password,
                    USER_ID: user_id,
                }
            )
        else:
            return JsonResponse(user_response)
    except json.JSONDecodeError as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


def get_broker_data_json(user_email, index):
    user_data = BrokerDetails.objects.filter(user_id=user_email, index_group=index)
    user_profiles_list = remove_data_from_list(list(user_data.values()))
    return user_profiles_list


def get_broker_details_using_id(user_email):
    try:
        # user_email = get_user_email(request)
        user_data = BrokerDetails.objects.filter(user_id=user_email)
        broker_data = list(user_data.values())
        broker_data = remove_data_from_list(broker_data)
        # user_profiles_list = get_broker_data_json(user_email,index)
        return JsonResponse({BROKER_DETAILS: broker_data})
    except json.JSONDecodeError as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


def get_broker_details_using_id_and_group(user_email, broker):
    try:
        user_data = BrokerDetails.objects.filter(user_id=user_email, broker_name=broker)
        broker_data = list(user_data.values())
        broker_data = remove_data_from_list(broker_data)[0]
        return JsonResponse({BROKER_DETAILS: broker_data})
    except json.JSONDecodeError as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


def get_index_group_name(data):
    try:
        if data != None:
            if len(data) > 0:
                return list(data.values())[0]["index_group"]
    except Exception as e:
        return GLOBAL_ERROR


def remove_data_from_list(updated_list):
    for data in updated_list:
        data.pop(ID)
        data.pop(USER_ID)
    return updated_list


def get_index_group_by_broker(all_brokers, user_broker):
    keys = []
    for key, values in all_brokers.items():
        if user_broker in values:
            keys.append(key)
    return keys


def current_time():
    current_datetime_utc = timezone.now()
    ist = pytz.timezone("Asia/Kolkata")
    current_time = current_datetime_utc.astimezone(ist).strftime("%Y-%m-%d %H:%M:%S")
    return current_time


def update_ltp_to_table(data):
    token = data["token"]
    data.pop("token")
    current_time_str = current_time()
    data["last_updated_time"] = current_time_str
    if str(data[LTP]) != 'None':
        updateIndexDetails(token, data)
    else:
        addLogDetails(ERROR, CONNECTION_ERROR)


def convert_string_to_int_array(string_array):
    int_array = [int(x) for x in string_array if x.isdigit()]
    return int_array


def getCurrentIndexValue(index):
    index_data = IndexDetails.objects.filter(index_name=index)
    index_data = list(index_data.values())[0]
    return float(index_data[LTP])
    # return int(input("Enter CurrentIndex value\n"))


def getCurrentIndexExpiry(index):
    index_data = IndexDetails.objects.filter(index_name=index)
    index_data = list(index_data.values())[0]
    return {
        CURRENT_EXPIRY: index_data[CURRENT_EXPIRY],
        NEXT_EXPIRY: index_data[NEXT_EXPIRY],
    }


def getIndexConfiguration(user_email, index):
    user_data = Configuration.objects.filter(user_id=user_email, index_name=index)
    user_profiles_list = list(user_data.values())
    remove_data_from_list(user_profiles_list)
    if len(user_profiles_list) > 0:
        return user_profiles_list[0]


def updateIndexConfiguration(user_email, index, data):
    try:
        user_data = Configuration.objects.filter(user_id=user_email, index_name=index)
        user_data.update(**data)
    except Exception as e:
        addLogDetails(ERROR, str(e))


def updateIndexDetails(token, data):
    try:
        index_data = IndexDetails.objects.filter(index_token=token)
        if index_data.update(**data) != 1:
            addLogDetails(INFO, "Error in db update")

    except Exception as e:
        addLogDetails(ERROR, str(e))


def addOrderBookDetails(data, is_entry):
    try:
        addLogDetails(INFO, "addOrderBookDetails")
        current_time_str = int(datetime.now().timestamp())
        # current_time_str=datetime.timestamp(datetime.now())
        if is_entry:
            data["entry_time"] = current_time_str
            data[STATUS] = ORDER_PLACED
            OrderBook.objects.create(**data)
        else:
            data[EXIT_TIME] = current_time_str
            user_data = OrderBook.objects.filter(
                user_id=data[USER_ID], script_name=data[SCRIPT_NAME], exit_price=None
            )
            order_info = list(user_data.values())[0]
            entry_price = order_info[ENTRY_PRICE]
            exit_price = data[EXIT_PRICE]
            qty = order_info[QTY]
            total = str(float((float(exit_price) - float(entry_price)) * int(qty)))
            data[TOTAL] = total
            user_data.update(**data)
        addLogDetails(INFO, "addOrderBookDetails : " + str(data))
        # if(list(user_data.values()) >0):

    except Exception as e:
        addLogDetails(ERROR, str(e))


def getTaregtForOrderFromList(levels, currentValue, orderType):
    try:
        if orderType == "CE":
            result = min(filter(lambda i: i > currentValue, levels), default=None)
            return result
        elif orderType == "PE":
            result = max(filter(lambda i: i < currentValue, levels), default=None)
            return result
    except Exception as e:
        addLogDetails(ERROR, str(e))


def convertDateString(dateStr):
    input_date_str = dateStr
    input_format = "%d%b%Y"
    output_format = "%d-%b-%Y"
    input_date = datetime.strptime(input_date_str, input_format)
    output_date_str = input_date.strftime(output_format)
    return output_date_str


def convertDateList(allExpiry):
    date_objects = [datetime.strptime(date_str, "%d%b%Y") for date_str in allExpiry]
    sorted_dates = sorted(date_objects)
    sorted_date_strings = [date.strftime("%d%b%Y").upper() for date in sorted_dates]
    return sorted_date_strings


def getnsedata(index_name):
    try:
        option_data = {}
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        df = pd.DataFrame.from_dict(requests.get(url).json())
        df = df[(df.name == index_name)]
        expiry_list = sorted(df.expiry.unique())
        expiry_list = [item for item in expiry_list if item != ""]
        expiry_list = convertDateList(expiry_list)
        option_data[0] = convertDateString(expiry_list[0])
        option_data[1] = convertDateString(expiry_list[1])
        return option_data
    except Exception as e:
        addLogDetails(ERROR, str(e))


@shared_task
def updateExpiryDetails():
    nifty = (
        str(NIFTY_DEFAULT_VALUES["index_name"])
        .replace("_", " ")
        .title()
        .replace(" ", "")
        .upper()
    )
    bank_nifty = (
        str(BANK_NIFTY_DEFAULT_VALUES["index_name"])
        .replace("_", " ")
        .title()
        .replace(" ", "")
        .upper()
    )
    fin_nifty = (
        str(FINNIFTY_DEFAULT_VALUES["index_name"])
        .replace("_", " ")
        .title()
        .replace(" ", "")
        .upper()
    )
    indexes = [nifty, bank_nifty, fin_nifty]
    for index in indexes:
        option_data = getnsedata(index)
        dataJson = {
            "current_expiry": str(option_data[0]).upper(),
            "next_expiry": str(option_data[1]).upper(),
        }
        addLogDetails(INFO, str(dataJson))
        if index == nifty:
            updateIndexDetails("99926000", dataJson)
        elif index == bank_nifty:
            updateIndexDetails("99926009", dataJson)
        elif index == fin_nifty:
            updateIndexDetails("99926037", dataJson)
    addLogDetails(INFO, "Expiry Updated")


def getExpiryList(index_name):
    try:
        expiry_details = getCurrentIndexExpiry(index_name)
        current_expiry = expiry_details[CURRENT_EXPIRY]
        next_expiry = expiry_details[NEXT_EXPIRY]
        if str(current_expiry).split("-")[1] != (str(next_expiry).split("-")[1]):
            expiry_details = {
                "current_expiry": current_expiry,
                "next_expiry": next_expiry,
                "is_monthly_expiry": True,
            }
        else:
            expiry_details = {
                "current_expiry": current_expiry,
                "next_expiry": next_expiry,
                "is_monthly_expiry": False,
            }
        return expiry_details
    except Exception as e:
        addLogDetails(INFO, "exception in getExpiryList  -----  " + str(e))


def getTradingSymbol(index_name):
    try:

        expiry_details = getExpiryList(index_name)
        current_expiry = expiry_details["current_expiry"]
        today = datetime.today()
        year = str(today.year)[2:4]
        month = str(current_expiry.split("-")[1])
        index_name = str(index_name).replace("_", "").upper()
        symbol = str(
            index_name + current_expiry.split("-")[0] + str(month) + year
        ).upper()
        return symbol
    except Exception as e:
        addLogDetails(INFO, "exception in getTradingSymbol  -----  " + str(e))


def getTokenUsingSymbol(symbol):
    try:
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        df = pd.DataFrame.from_dict(requests.get(url).json())
        df = df[(df.symbol == symbol)]
        token = df.iloc[0]["token"]
        return token
    except Exception as e:
        addLogDetails(ERROR, str(e))


def getDisplayName(value):
    words = value.split("_")
    title_case_str = " ".join(word.capitalize() for word in words)
    return title_case_str


def is_integer(value):
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False


def is_float(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def validate_levels(data):
    if LEVELS in data and not validate_levels(data[LEVELS]):
        pattern = re.compile(r"^[0-9,.]+$")
        if not pattern.match(data[LEVELS]):
            raise ValueError(INCORRECT_INPUT + getDisplayName(LEVELS))


def remove_spaces_from_json(data):
    data_str = json.dumps(data)
    return json.loads(data_str.replace(" ", ""))


def validate_numeric_fields(data):
    numeric_fields = [STRIKE, LOTS]
    for field in numeric_fields:
        if field in data and not is_integer(data[field]):
            raise ValueError(INCORRECT_INPUT + getDisplayName(field))


def validate_float_field(data):
    float_field = [
        TREND_CHECK_POINTS,
        TRAILING_POINTS,
        INITIAL_SL,
        SAFE_SL,
        TARGET_FOR_SAFE_SL,
    ]
    for field in float_field:
        if field in data and not is_float(data[field]):
            raise ValueError(INCORRECT_INPUT + getDisplayName(field))


def validate_char_fields(data):
    char_fields = [BROKER_QR, BROKER_USER_ID, BROKER_USER_NAME, BROKER_MPIN, BROKER_API_TOKEN]
    for field in char_fields:
        if field in data:
            pattern = re.compile(r'^[A-Za-z0-9 ]+$')
            if not pattern.match(data[field]):
                raise ValueError(INCORRECT_INPUT + getDisplayName(field))


log_file_path = os.path.join(os.getcwd(), 'madara.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def addLogDetails(log_type, logDetails):
    print(logDetails)
    if str(log_type).__eq__("info"):
        logging.info(logDetails)
    elif str(log_type).__eq__("error"):
        logging.error(logDetails)


def is_time_less_than_current_time(time_string):
    now = datetime.strptime(time_string, "%H:%M").time()
    target_time = datetime.strptime("09:15", "%H:%M").time()

    if now < target_time:
        print("The current time is less than 09:15 AM.")
        return True
    else:
        print("The current time is 09:15 AM or later.")
        return False


def increaseTime(datetime_str, minutes):
    try:
        print("into increasetime")
        # datetime_str = "2024-06-28 09:15"
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        new_datetime_obj = datetime_obj + timedelta(minutes=minutes)
        new_datetime_str = new_datetime_obj.strftime("%Y-%m-%d %H:%M")
        return new_datetime_str
    except Exception as e:
        print(e)

@shared_task
def terminate_task(user_email, index,strategy):
    try:
        user_data = JobDetails.objects.filter(user_id=user_email, index_name=index,strategy=strategy)
        job_details = list(user_data.values())
        if len(job_details) > 0:
            task_id = job_details[0]['job_id']
            result = AsyncResult(str(task_id))
            result.revoke(terminate=True)
            if user_data.exists():
                user_data.delete()
                updateIndexConfiguration(user_email, index, data=STAGE_STOPPED)

                return JsonResponse({STATUS: SUCCESS, MESSAGE: "Index Stopped"})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: "Index not running"})

    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})