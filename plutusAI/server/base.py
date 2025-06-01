import json
import logging
import os
import re
import time
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.utils import timezone
import pandas as pd
import requests
from plutusAI.models import *
from plutusAI.server import AngelOneApp
from plutusAI.server.constants import *
import pytz
from celery import shared_task
from celery.result import AsyncResult
from logging.handlers import TimedRotatingFileHandler
from concurrent.futures import ThreadPoolExecutor, as_completed



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

def add_broker_details(data_json):
    BrokerDetails.objects.create(
        user_id=data_json.get("user_id"),
        broker_user_id=data_json.get("broker_user_id"),
        broker_user_name=data_json.get("broker_user_name"),
        broker_name=data_json.get("broker_name"),
        token_status=data_json.get("token_status"),
        is_demo_trading_enabled=data_json.get("is_demo_trading_enabled"),
        broker_api_token=data_json.get("broker_api_token"),
        broker_mpin=data_json.get("broker_mpin"),
        broker_qr=data_json.get("broker_qr"),
        index_group=data_json.get("index_group")
    )
def add_manual_order(data_json):
    ManualOrders.objects.create(
        user_id=data_json.get("user_id"),
        index_name=data_json.get("index_name"),
        target=data_json.get("target"),
        stop_loss=data_json.get("stop_loss"),
        order_status=data_json.get("order_status"),
        time=data_json.get("time"),
        strike=data_json.get("strike"),
        lots=data_json.get("lots"),
        trigger=data_json.get("trigger"),

    )


def add_scalper_details(data_json):
    ScalperDetails.objects.create(
        user_id=data_json.get("user_id"),
        index_name=data_json.get("index_name"),
        strike=data_json.get("strike"),
        is_demo_trading_enabled=data_json.get("is_demo_trading_enabled"),
        use_full_capital=data_json.get("use_full_capital"),
        target=data_json.get("target"),
        lots=data_json.get("lots"),
        on_candle_close=data_json.get("on_candle_close"),
        status=data_json.get("status")
    )
def add_flash_details(data_json):
    FlashDetails.objects.create(
        user_id=data_json.get("user_id"),
        index_name=data_json.get("index_name"),
        strike=data_json.get("strike"),
        max_profit=data_json.get("max_profit"),
        max_loss=data_json.get("max_loss"),
        trend_check_points=data_json.get("trend_check_points"),
        trailing_points=data_json.get("trailing_points"),
        is_demo_trading_enabled=data_json.get("is_demo_trading_enabled"),
        lots=data_json.get("lots"),
        status=data_json.get("status"),
        average_points=data_json.get("average_points")
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


# def add_user_and_populate_data(user_data):
#     try:
#         user_id = user_data.get(USER_ID)
#         user_password = user_data.get(PASSWORD)
#         username = str(user_id).split("@")[0]
#         password = user_password
#         user_details = add_user(username, user_id, password)
#         user_response = json.loads(user_details.content)
#         addLogDetails(INFO, f"New user added Response:  {user_response}")
#
#         if user_response.get(MESSAGE).__eq__(USER_ADDED):
#             addAllIndexValues(user_id)
#             broker_sample_data_json["user_id"] = user_id
#             add_broker_details(broker_sample_data_json)
#             scalper_data_json["user_id"] = user_id
#             add_scalper_details(scalper_data_json)
#             webhook_data_json["user_id"] = user_id
#             add_webhook_details(webhook_data_json)
#             for order_data in manual_orders_sample_data:
#                 order_data["user_id"] = user_id
#                 add_manual_order(order_data)
#
#             return JsonResponse(
#                 {
#                     STATUS: SUCCESS,
#                     MESSAGE: "User added",
#                     USER_NAME: username,
#                     PASSWORD: password,
#                     USER_ID: user_id,
#                 }
#             )
#         else:
#             return JsonResponse(user_response)
#     except json.JSONDecodeError as e:
#         return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON})
#     except Exception as e:
#         addLogDetails(ERROR, str(e))
#         return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})
def add_user_and_populate_data(user_data):
    try:
        user_id = user_data.get("email")
        user_password = user_data.get(PASSWORD)
        if not user_id or not user_password:
            return JsonResponse({STATUS: FAILED, MESSAGE: "Missing user_id or password"})
        username = str(user_id).split("@")[0]
        password = user_password
        user_details = add_user(username, user_id, password)
        user_response = json.loads(user_details.content)
        addLogDetails(INFO, f"New user added Response: {user_response}")
        if user_response.get(MESSAGE) == USER_ADDED:
            addAllIndexValues(user_id)
            broker_data = broker_sample_data_json.copy()
            broker_data["user_id"] = user_id
            add_broker_details(broker_data)
            scalper_data = scalper_data_json.copy()
            scalper_data["user_id"] = user_id
            add_scalper_details(scalper_data)
            flash_data = flash_sample_data_json.copy()
            flash_data["user_id"] = user_id
            add_flash_details(flash_data)
            for order_data in manual_orders_sample_data:
                order = order_data.copy()
                order["user_id"] = user_id
                add_manual_order(order)
            return JsonResponse({
                STATUS: SUCCESS,
                MESSAGE: "User added",
                USER_NAME: username,
                PASSWORD: password,
                USER_ID: user_id,
            })
        else:
            return JsonResponse(user_response)
    except json.JSONDecodeError:
        return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


def get_broker_data_json(user_email, index):
    user_data = BrokerDetails.objects.filter(user_id=user_email, index_group=index)
    user_profiles_list = remove_data_from_list(list(user_data.values()))
    return user_profiles_list


def get_broker_details_json_using_id(user_email):
    user_data = BrokerDetails.objects.filter(user_id=user_email)
    broker_data = list(user_data.values())
    broker_data = remove_data_from_list(broker_data)
    return broker_data


def get_broker_details_using_id(user_email):
    try:
        # user_email = get_user_email(request)
        broker_data = get_broker_details_json_using_id(user_email)
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


def updateScalperDetails(user_email, index, data):
    try:
        user_data = ScalperDetails.objects.filter(user_id=user_email, index_name=index)
        user_data.update(**data)
    except Exception as e:
        addLogDetails(ERROR, str(e))

def updateFlashConfiguration(user_email, index, data):
    try:
        user_data = FlashDetails.objects.filter(user_id=user_email, index_name=index)
        user_data.update(**data)
    except Exception as e:
        addLogDetails(ERROR, str(e))

def updateIndexDetails(token, data):
    try:
        index_data = IndexDetails.objects.filter(index_token=token)
        if len(index_data.values()) ==0:
            print("no Data in table")
            print(data)
            index_data = IndexDetails.objects.filter(index_name=data[INDEX_NAME])
            index_data.update(**data)
        elif index_data.update(**data) != 1:
            addLogDetails(INFO, "Error in db update")

    except Exception as e:
        addLogDetails(ERROR, str(e))


def addOrderBookDetails(data, is_entry):
    try:
        addLogDetails(INFO, "addOrderBookDetails")
        current_time_str = getCurrentTimestamp()
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


# def getnsedata(index_name):
#     try:
#         option_data = {}
#         url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
#         df = pd.DataFrame.from_dict(requests.get(url).json())
#         df = df[(df.name == index_name)]
#         expiry_list = sorted(df.expiry.unique())
#         expiry_list = [item for item in expiry_list if item != ""]
#         expiry_list = convertDateList(expiry_list)
#         option_data[0] = convertDateString(expiry_list[0])
#         option_data[1] = convertDateString(expiry_list[1])
#         return option_data
#     except Exception as e:
#         addLogDetails(ERROR, str(e))

def getnsedata(index_names):
    try:
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        df = pd.DataFrame.from_dict(response.json())
        result = {}
        for index_name in index_names:
            index_df = df[df.name == index_name]
            expiry_list = sorted(filter(None, index_df.expiry.unique()))
            expiry_list = convertDateList(expiry_list)
            if len(expiry_list) < 2:
                addLogDetails(ERROR, f"Insufficient expiry data for index: {index_name}")
                continue
            result[index_name] = {
                "current_expiry": convertDateString(expiry_list[0]),
                "next_expiry": convertDateString(expiry_list[1]),
            }
        return result
    except Exception as e:
        addLogDetails(ERROR, f"getnsedata error: {str(e)}")
        return {}


def get_last_thursday(year: int, month: int) -> str:
    """
    Returns the last Thursday of the given month as a string in 'DDMMMYYYY' format.
    If today's date is after the last Thursday, returns the last Thursday of next month.
    """
    today = datetime.now()

    # Find last Thursday of the given month
    if month == 12:
        last_day = datetime(year, 12, 31)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)

    while last_day.weekday() != 3:  # 3 = Thursday
        last_day -= timedelta(days=1)

    # If today is after last Thursday, get next month's last Thursday
    if today > last_day:
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1

        # Find last Thursday of next month
        if month == 12:
            last_day = datetime(year, 12, 31)
        else:
            last_day = datetime(year, month + 1, 1) - timedelta(days=1)

        while last_day.weekday() != 3:
            last_day -= timedelta(days=1)

    return last_day.strftime("%d%b%Y").upper()

# def get_futures_expiry_json(index_name, instrumenttype, exch_seg):
#     try:
#         url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
#         df = pd.DataFrame(requests.get(url).json())
#
#         # Filter for index
#         df_filtered = df[
#             (df["name"] == index_name) &
#             (df["instrumenttype"] == instrumenttype) &
#             (df["exch_seg"] == exch_seg)
#         ].copy()
#
#         # Dates for current and next month expiry
#         today = datetime.now()
#         print(df_filtered)
#         current_expiry_str = get_last_thursday(today.year, today.month)
#         print(current_expiry_str)
#         next_month = today.month + 1 if today.month < 12 else 1
#         next_year = today.year if today.month < 12 else today.year + 1
#         next_expiry_str = get_last_thursday(next_year, next_month)
#
#         current_row = df_filtered[df_filtered["expiry"].str.upper() == current_expiry_str]
#         next_row = df_filtered[df_filtered["expiry"].str.upper() == next_expiry_str]
#         print(current_row)
#         if current_row.empty or next_row.empty:
#             return {"error": f"Futures data not found for {index_name}"}
#
#         current_data = current_row.iloc[0]
#         next_data = next_row.iloc[0]
#
#         return {
#             "current_expiry": datetime.strptime(current_data["expiry"], "%d%b%Y").strftime("%d-%b-%Y"),
#             "next_expiry": datetime.strptime(next_data["expiry"], "%d%b%Y").strftime("%d-%b-%Y"),
#             "index_token": str(current_data["token"]),
#             "symbol": current_data["symbol"],
#             "name": current_data["name"],
#             "lotsize": str(current_data["lotsize"])
#         }
#
#     except Exception as e:
#         return {"error": str(e)}


def get_next_futures_expiry(index_name: str, instrumenttype: str, exch_seg: str) -> str:
    """
    Uses the actual expiry dates from AngelOne's OpenAPIScripMaster.json to find the next expiry.
    """
    try:
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        df = pd.DataFrame(requests.get(url).json())

        df_filtered = df[
            (df["name"] == index_name) &
            (df["instrumenttype"] == instrumenttype) &
            (df["exch_seg"] == exch_seg)
            ].copy()

        # Convert expiry strings to datetime
        df_filtered["expiry_date"] = pd.to_datetime(df_filtered["expiry"], format="%d%b%Y", errors="coerce")
        df_filtered = df_filtered.dropna(subset=["expiry_date"])

        # Get current and next expiry after today
        today = datetime.now()
        future_expiries = df_filtered[df_filtered["expiry_date"] >= today].sort_values("expiry_date")

        if len(future_expiries) < 2:
            return {"error": f"Not enough expiry data for {index_name}"}

        current_data = future_expiries.iloc[0]
        next_data = future_expiries.iloc[1]

        return {
            "current_expiry": current_data["expiry_date"].strftime("%d-%b-%Y"),
            "next_expiry": next_data["expiry_date"].strftime("%d-%b-%Y"),
            "index_token": str(current_data["token"]),
            "symbol": current_data["symbol"],
            "name": current_data["name"],
            "lotsize": str(current_data["lotsize"])
        }

    except Exception as e:
        return f"Error: {e}"




@shared_task
def updateExpiryDetails():
    name = "BANKNIFTY"
    instrumenttype = "FUTIDX"
    exch_seg = "NFO"

    nifty = str(NIFTY_DEFAULT_VALUES["index_name"]).replace("_", " ").title().replace(" ", "").upper()
    bank_nifty = str(BANK_NIFTY_DEFAULT_VALUES["index_name"]).replace("_", " ").title().replace(" ", "").upper()
    fin_nifty = str(FINNIFTY_DEFAULT_VALUES["index_name"]).replace("_", " ").title().replace(" ", "").upper()


    index_map = {
        nifty: "99926000",
        bank_nifty: "99926009",
        fin_nifty: "99926037",
    }
    expiry_data = getnsedata(list(index_map.keys()))

    for index_name, data in expiry_data.items():
        addLogDetails(INFO, f"{index_name} Expiry: {data}")
        updateIndexDetails(index_map[index_name], data)
        #####
    bank_nifty_fut_data = get_next_futures_expiry(name, instrumenttype, exch_seg)
    print(bank_nifty_fut_data)
    bank_nifty_fut_data_json = {"current_expiry": str(bank_nifty_fut_data["current_expiry"]).upper(),
                                "next_expiry": str(bank_nifty_fut_data["next_expiry"]).upper(),
                                INDEX_NAME: 'bank_nifty_fut', "index_token": bank_nifty_fut_data["index_token"],
                                "qty": bank_nifty_fut_data["lotsize"]}

    updateIndexDetails(bank_nifty_fut_data['index_token'], bank_nifty_fut_data_json)

    addLogDetails(INFO, "Expiry Updated")


# def updateExpiryDetails():
#     nifty = (
#         str(NIFTY_DEFAULT_VALUES["index_name"])
#         .replace("_", " ")
#         .title()
#         .replace(" ", "")
#         .upper()
#     )
#     bank_nifty = (
#         str(BANK_NIFTY_DEFAULT_VALUES["index_name"])
#         .replace("_", " ")
#         .title()
#         .replace(" ", "")
#         .upper()
#     )
#     fin_nifty = (
#         str(FINNIFTY_DEFAULT_VALUES["index_name"])
#         .replace("_", " ")
#         .title()
#         .replace(" ", "")
#         .upper()
#     )
#     indexes = [nifty, bank_nifty, fin_nifty]
#     for index in indexes:
#         option_data = getnsedata(index)
#         dataJson = {
#             "current_expiry": str(option_data[0]).upper(),
#             "next_expiry": str(option_data[1]).upper(),
#         }
#         addLogDetails(INFO, str(dataJson))
#         if index == nifty:
#             updateIndexDetails("99926000", dataJson)
#         elif index == bank_nifty:
#             updateIndexDetails("99926009", dataJson)
#         elif index == fin_nifty:
#             updateIndexDetails("99926037", dataJson)
#     addLogDetails(INFO, "Expiry Updated")


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


# log_file_path = os.path.join(os.getcwd(), 'madara.log')
# logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#
#
# def addLogDetails(log_type, logDetails):
#     logging.basicConfig()
#     print(logDetails)
#     if str(log_type).__eq__("info"):
#         logging.info(logDetails)
#     elif str(log_type).__eq__("error"):
#         logging.error(logDetails)

# Define the log file path
log_file_path = os.path.join(os.getcwd(), 'madara.log')


# Custom formatter to include timezone in log timestamps
class TimezoneFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, tzname='Asia/Kolkata'):
        super().__init__(fmt, datefmt)
        self.tz = pytz.timezone(tzname)

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=self.tz)
        if datefmt:
            return dt.strftime(datefmt)
        else:
            return dt.isoformat()


# Create a handler for rotating logs
handler = TimedRotatingFileHandler(
    log_file_path, when='midnight', interval=1, backupCount=7
)

# Create a custom formatter with timezone
formatter = TimezoneFormatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S %Z')
handler.setFormatter(formatter)

# Configure logging
logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
)


def addLogDetails(log_type, logDetails):
    print(logDetails)
    if log_type == "info":
        logging.info(logDetails)
    elif log_type == "error":
        logging.error(logDetails)
    else:
        logging.warning(f"Unknown log type: {log_type}. Log details: {logDetails}")


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
def terminate_task(user_email, index, strategy):
    try:
        addLogDetails(INFO, f"terminate_task for {user_email} index {index} strategy {strategy}")
        user_data = JobDetails.objects.filter(user_id=user_email, index_name=index, strategy=strategy)
        job_details = list(user_data.values())
        if strategy == STRATEGY_HUNTER:
            updateIndexConfiguration(user_email, index, data=STAGE_STOPPED)
        else:
            updateScalperDetails(user_email, index, data=STAGE_STOPPED)
        if len(job_details) > 0:
            task_id = job_details[0]['job_id']
            user_data.delete()
            addLogDetails(INFO, "Job Deleted")
            result = AsyncResult(str(task_id))
            result.revoke(terminate=True)
            addLogDetails(INFO, "Job Terminated")
            return JsonResponse({STATUS: SUCCESS, MESSAGE: "Index Stopped", "task_status": False})
        else:
            return JsonResponse({STATUS: FAILED, MESSAGE: "Index not running"})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


def checkSocketStatus():
    user_data = JobDetails.objects.filter(
        user_id=ADMIN_USER_ID, index_name=SOCKET_JOB, strategy=SOCKET_JOB
    )
    if user_data.count() > 0:
        return JsonResponse({STATUS: FAILED, MESSAGE: "Socket running"})
    else:
        start_ws_job(SOCKET_JOB_TYPE)
        return JsonResponse({STATUS: SUCCESS, MESSAGE: "Socket Job started"})


def start_ws_job(ws_type):
    try:
        updateExpiryDetails.delay()
        if ws_type is None or ws_type.__eq__("1"):
            # AngelOneApp.createV1Socket.delay()
            AngelOneApp.createAngleOneCandle.delay()
        elif ws_type.__eq__("2"):
            # AngelOneApp.createAngleOne.delay()
            AngelOneApp.createHttpData.delay()
        elif ws_type.__eq__("3"):
            AngelOneApp.angelOneWSNSE.delay()
        # elif ws_type.__eq__("3"):
        #     AngelOneApp.createHttpData.delay()
        # elif ws_type.__eq__("4"):
        #     AngelOneApp.createAngleOneCandle.delay()

        return JsonResponse({STATUS: SUCCESS, MESSAGE: "WS started", "task_status": True})
    except json.JSONDecodeError as e:
        return JsonResponse({STATUS: FAILED, MESSAGE: INVALID_JSON})
    except Exception as e:
        addLogDetails(ERROR, str(e))
        return JsonResponse({STATUS: FAILED, MESSAGE: GLOBAL_ERROR})


def get_next_minute_start():
    # now = datetime.datetime.now()
    # next_minute_start = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
    # if now.second >= 59:  # Adjust based on your requirement
    #     next_minute_start += datetime.timedelta(minutes=1)
    # return next_minute_start
    import datetime
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    now_kolkata = datetime.datetime.now(kolkata_tz)
    next_minute_start = now_kolkata.replace(second=0, microsecond=0) + datetime.timedelta(minutes=1,seconds=00,milliseconds=000,microseconds=000)
    timestamp_ms = int(next_minute_start.timestamp() * 1000)
    return timestamp_ms

def get_current_minute_start():

    import datetime
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    now_kolkata = datetime.datetime.now(kolkata_tz)
    next_minute_start = now_kolkata.replace(second=0, microsecond=0)
    timestamp_ms = int(next_minute_start.timestamp() * 1000)
    return timestamp_ms

def get_previous_minute_start(current_time_ms,with_sec):
    import datetime
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    timestamp_sec = current_time_ms / 1000
    date_kolkata = datetime.datetime.fromtimestamp(timestamp_sec, kolkata_tz) - datetime.timedelta(minutes=1,seconds=00)
    if with_sec:
        return_date = date_kolkata.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return_date = date_kolkata.strftime('%Y-%m-%d %H:%M')
    # print(return_date)
    return return_date

def get_previous_n_minute_start(current_time_ms,with_sec,minute):
    import datetime
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    timestamp_sec = current_time_ms / 1000
    date_kolkata = datetime.datetime.fromtimestamp(timestamp_sec, kolkata_tz) - datetime.timedelta(minutes=minute,seconds=00)
    if with_sec:
        return_date = date_kolkata.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return_date = date_kolkata.strftime('%Y-%m-%d %H:%M')
    # print(return_date)
    return return_date

def get_next_minute_start_ms(current_time_ms,with_sec):
    import datetime
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    timestamp_sec = current_time_ms / 1000
    date_kolkata = datetime.datetime.fromtimestamp(timestamp_sec, kolkata_tz) + datetime.timedelta(minutes=1,seconds=00)
    if with_sec:
        return_date = date_kolkata.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return_date = date_kolkata.strftime('%Y-%m-%d %H:%M')
    # print(return_date)
    return return_date


# Function to format time in HH:MM:SS
def format_time(current_time_ms):
    import datetime
    timestamp_sec = current_time_ms / 1000
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    date_kolkata = datetime.datetime.fromtimestamp(timestamp_sec, kolkata_tz)
    return date_kolkata.strftime('%Y-%m-%d %H:%M:%S')

def format_time_in_min(current_time_ms):
    import datetime
    timestamp_sec = current_time_ms / 1000
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    date_kolkata = datetime.datetime.fromtimestamp(timestamp_sec, kolkata_tz)
    return date_kolkata.strftime('%Y-%m-%d %H:%M')

def getCurrentIndexClose(index, start_date, end_date):
    index_data = IndexDetails.objects.filter(index_name=index)
    index_data = list(index_data.values())[-1]
    return float(index_data[CLOSE])


def update_candle_data_to_table(candle_data):
    # candle_data = {"token": token, "index_name": data[TRADING_SYMBOL], "time": format_time(start_time_dict[token]),
    #                "open": open_price, "high": high_price, "low": low_price, "close": close_price}
    print(candle_data)

    token = candle_data["token"]
    candle_data.pop("token")
    # current_time_str = current_time()
    # candle_data["time"] = current_time_str

    if str(candle_data[CLOSE]) != 'None':
        CandleData.objects.create(
            index_name="bank_nifty_fut",
            token=token,
            time=candle_data["time"],
            open=candle_data["open"],
            high=candle_data["high"],
            low=candle_data["low"],
            close=candle_data["close"]
        )
    else:
        addLogDetails(ERROR, CONNECTION_ERROR)


def convert_datetime_string(datetime_str):
    from datetime import datetime
    format_str = '%Y-%m-%d %H:%M'
    dt = datetime.strptime(datetime_str, format_str)
    dt_dict = {
        'year': dt.year,
        'month': dt.month,
        'day': dt.day,
        'hour': dt.hour,
        'minute': dt.minute,
        'second': dt.second
    }

    return dt_dict


def getCurrentTimestamp():
    return str(datetime.now().timestamp())


def getBrokerageForLots(lots,qty):
    broker_price = 20
    exchange_tax = 3.4081
    stamp_charges = 0.2066
    sebi_fee = 0.0069
    base_gst = 4.2
    runtime_gst = 0.6
    total_charges = (int(lots) * (exchange_tax + stamp_charges + sebi_fee + runtime_gst)) + base_gst + broker_price
    brokerage = float(2*(total_charges/(int(lots)*int(qty))))
    return brokerage

def getUserOrderBookDetails(user_email,index_name,is_today):
    try:
        if is_today:
            start_of_day_timestamp = int(
                time.mktime(time.strptime(time.strftime("%Y-%m-%d 00:00:00"), "%Y-%m-%d %H:%M:%S")))
            ob_data = OrderBook.objects.filter(user_id=user_email,index_name=index_name , exit_time__gte=start_of_day_timestamp).values('strategy').annotate(total_sum=Sum('total'))

        else:
            ob_data = OrderBook.objects.filter(user_id=user_email, index_name=index_name).values('strategy').annotate(total_sum=Sum('total'))
        totals_by_strategy = {}
        for record in ob_data:
            strategy = record['strategy']
            total = float(record['total_sum'])
            totals_by_strategy[strategy] = totals_by_strategy.get(strategy, 0) + total

        json_result = json.dumps(totals_by_strategy, cls=DjangoJSONEncoder)
        return json_result

    except Exception as e:
        # Handle exceptions, e.g., log the error or return a default response
        return addLogDetails(ERROR,str(e))

def getUserDashboardDetails(user_email,is_today):
    index = INDECES
    all_data = {}
    for index_name in index:
        ob_data = getUserOrderBookDetails(user_email, index_name,is_today)
        print(ob_data)
        print(ob_data.upper().__contains__(index_name))
        all_data[index_name] = ob_data
    return all_data

def updateManualOrderDetails(user_email, index, data):
    try:
        user_data = ManualOrders.objects.filter(user_id=user_email, index_name=index)
        user_data.update(**data)
    except Exception as e:
        addLogDetails(ERROR, str(e))

def getManualOrderDetails(user_email, index):
    try:
        user_data = ManualOrders.objects.filter(user_id=user_email, index_name=index)
        user_data=list(user_data.values())[0]
        return user_data
    except Exception as e:
        addLogDetails(ERROR, str(e))

# def updateWebhookOrderDetails(user_email, index,strategy, data):
#     try:
#         user_data = WebhookDetails.objects.filter(user_id=user_email, index_name=index,strategy=strategy)
#         user_data.update(**data)
#     except Exception as e:
#         addLogDetails(ERROR, str(e))


def addWebhookOrderDetails(user_email, index,strategy, data):
    try:
        addLogDetails(INFO, "addWebhookOrderDetails")
        current_time_str = getCurrentTimestamp()
        data["time"] = current_time_str
        data[USER_ID]= user_email
        data[INDEX_NAME] = index
        data[STRATEGY] = strategy
        data["order_status"] = ORDER_PLACED
        user_data = WebhookDetails.objects.filter(user_id=user_email, index_name=index, strategy=strategy)
        if len(list(user_data.values())) <= 0:
            WebhookDetails.objects.create(**data)
        else:
            user_data.update(**data)
        addLogDetails(INFO, "addWebhookOrderDetails : " + str(data))

    except Exception as e:
        addLogDetails(ERROR, str(e))


from datetime import datetime
from django.db.models import Count, Sum, F, ExpressionWrapper, FloatField
from django.utils.timezone import now

def getStrategySummaryUsingEmail(user_email):
    BROKERAGE_PER_ORDER = 70
    current_date = now().date()  # Get today's date

    try:
        user = User.objects.get(email=user_email)
        user_name = user.username
        # Fetch all available data
        full_summary = OrderBook.objects.filter(user_id=user_email).values(
            'strategy', 'index_name'
        ).annotate(
            order_count=Count('id'),
            total_profit=ExpressionWrapper(Sum('total') - Count('id') * BROKERAGE_PER_ORDER, output_field=FloatField())
        ).order_by('-total_profit')

        # Fetch only today's data
        today_summary = OrderBook.objects.filter(
            user_id=user_email
        ).annotate(
            entry_date=ExpressionWrapper(F('entry_time'), output_field=FloatField())  # Keep entry_time as float
        ).filter(
            entry_date__gte=datetime.combine(current_date, datetime.min.time()).timestamp(),
            entry_date__lt=datetime.combine(current_date, datetime.max.time()).timestamp()
        ).values(
            'strategy', 'index_name'
        ).annotate(
            order_count=Count('id'),
            total_profit=ExpressionWrapper(Sum('total') - Count('id') * BROKERAGE_PER_ORDER, output_field=FloatField())
        ).order_by('-total_profit')
        total_orders_today = today_summary.aggregate(total=Sum('order_count'))['total'] or 0

        return {
            "status": "success",
            "full_summary": list(full_summary),  # All available data
            "current_day_summary": list(today_summary),  # Only today's data
            "current_date": current_date.strftime("%Y-%m-%d"),
            "task_status": True,
            "user_name":user_name,
            "total_orders_today": total_orders_today
        }

    except Exception as e:
        addLogDetails(ERROR, f"Error in getStrategySummaryUsingEmail: {str(e)}")

    return {
        "status": "error",
        "full_summary": [],
        "current_date_summary": [],
        "current_date": current_date.strftime("%Y-%m-%d"),
        "task_status": False
    }

def getOpenOrdersUsingEmail(user_email,broker):
    open_orders = OrderBook.objects.filter(user_id=user_email, exit_price__isnull=True)

    # Prepare order data as dicts for easier parallel processing
    order_dicts = []
    for order in open_orders:
        order_dicts.append({
            "entry_time": order.entry_time,
            "exit_time": order.exit_time,
            "script_name": order.script_name,
            "qty": order.qty,
            "entry_price": order.entry_price,
            "exit_price": order.exit_price,
            "status": order.status,
            "total": order.total,
            "strategy": order.strategy,
            "index_name": order.index_name,
        })

    # Worker function: do NOT modify broker.getLtpForPremium itself
    def get_ltp_for_order(order):
        option_details = broker.getCurrentPremiumDetails(NFO, order["script_name"])
        ltp = broker.getLtpForPremium(option_details)  # using the same call
        order["ltp"] = ltp
        return order

    orders_with_ltp = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_ltp_for_order, order) for order in order_dicts]
        for future in as_completed(futures):
            orders_with_ltp.append(future.result())

    return JsonResponse({OPEN_ORDERS:orders_with_ltp}, safe=False)