# import datetime
# import time

# import pytz
from SmartApi import  SmartWebSocket
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from plutusAI.server.base import *
from plutusAI.server.broker.AngelOneBroker import AngelOneBroker
from plutusAI.server.constants import *
from celery import current_task

import datetime
# from datetime import datetime, time

@shared_task
def createAngleOne():
    # API_KEY = "Q12feFjR"
    # CLIENT_CODE = "S50761409"
    # pwd_pin = "1005"
    # smartApi = SmartConnect(API_KEY)
    # qr_token = "5TXNGVJEVZYMHCLF6HHOQHHTZ4"
    # totp = pyotp.TOTP(qr_token).now()

    #
    # data = smartApi.generateSession(CLIENT_CODE, pwd_pin, totp)
    # AUTH_TOKEN = data['data']['jwtToken']
    # refreshToken = data['data']['refreshToken']
    # FEED_TOKEN = data['data']['feedToken']
    #
    # # fetch the feedtoken
    # feedToken = smartApi.getfeedToken()
    # userProfile = smartApi.getProfile(refreshToken)
    task_id = current_task.request.id
    JobDetails.objects.create(
        user_id=ADMIN_USER_ID,
        index_name=SOCKET_JOB,
        job_id=task_id,
        strategy=SOCKET_JOB
    )
    user_broker_data = BrokerDetails.objects.filter(user_id=ADMIN_USER_ID, index_group=INDIAN_INDEX)
    BrokerObject = AngelOneBroker(user_broker_data)
    correlation_id = "admin_ws"
    mode = None
    token_list = None

    def createWebSocketObj(token, exchangeType):
        global mode
        global token_list
        action = 1
        mode = 1

        token_list = [
            {
                "exchangeType": exchangeType,
                "tokens": token
            }
        ]
        swsObj = SmartWebSocketV2(BrokerObject.auth_token, BrokerObject.broker_api_token, BrokerObject.broker_user_id,
                                  BrokerObject.feed_token, max_retry_attempt=10)
        return swsObj

    sws = None

    def on_data(wsapp, message):
        data = {'token': message['token'], 'ltp': str(message['last_traded_price'] / 100)}
        print(data)
        update_ltp_to_table(data)
        time.sleep(0.5)

    def on_open(wsapp):
        addLogDetails(INFO, "on open WS2")
        global mode
        global token_list
        sws.subscribe(correlation_id, mode, token_list)
        # sws.unsubscribe(correlation_id, mode, token_list1)

    def on_error(wsapp, error):
        addLogDetails(ERROR, str(error))

    def on_close(wsapp):
        addLogDetails(INFO, "Close")

    def close_connection():
        sws.close_connection()
        addLogDetails(INFO, "close_connection")

    ## 26000,26009,26037
    sws = createWebSocketObj([99926000, 99926009, 99926037], 1)
    # sws = createWebSocketObj([99926000], 1)

    # Assign the callbacks.
    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error
    sws.on_close = on_close

    # Need to use after glitches in API resoved
    sws.connect()


@shared_task
def createHttpData():
    task_id = current_task.request.id
    JobDetails.objects.create(
        user_id=ADMIN_USER_ID,
        index_name=HTTP_JOB,
        job_id=task_id,
        strategy=HTTP_JOB
    )
    user_broker_data = BrokerDetails.objects.filter(user_id=ADMIN_USER_ID, index_group=INDIAN_INDEX)
    BrokerObject = AngelOneBroker(user_broker_data)
    allData = []
    niftyData = BrokerObject.getCurrentPremiumDetails(NSE, NIFTY_50)  # "Nifty 50"
    BNData = BrokerObject.getCurrentPremiumDetails(NSE, NIFTY_BANK)
    FNData = BrokerObject.getCurrentPremiumDetails(NSE, NIFTY_FIN_SERVICE)
    # BNFUT_DATA=BrokerObject.getTokenForSymbol(BANKNIFTY_FUTURES)
    allData.append(niftyData)
    allData.append(BNData)
    allData.append(FNData)
    # allData.append(BNFUT_DATA)
    addLogDetails(INFO, "Expiry Details updated from createHttpData")
    addLogDetails(INFO, allData)
    while True:
        for data in allData:
            value = {TOKEN: data[SYMBOL_TOKEN], LTP: str(BrokerObject.getLtpForPremium(data))}
            # print(value)
            if value[LTP] is not None:
                update_ltp_to_table(value)
                time.sleep(1)


@shared_task
def createV1Socket():
    user_broker_data = BrokerDetails.objects.filter(user_id=ADMIN_USER_ID, index_group=INDIAN_INDEX)
    BrokerObject = AngelOneBroker(user_broker_data)
    FEED_TOKEN = "092017047"
    CLIENT_CODE = "S212741"
    # token="mcx_fo|224395"
    token = "nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045"
    # token="mcx_fo|226745&mcx_fo|220822&mcx_fo|227182&mcx_fo|221599"
    task = "mw"
    ss = SmartWebSocket(BrokerObject.feed_token, CLIENT_CODE)

    def on_message(ws, message):
        addLogDetails(INFO , "Ticks: {}".format(message))

    def on_open(ws):
        addLogDetails(INFO, "on open WS V1")
        ss.subscribe(task, token)

    def on_error(ws, error):
        addLogDetails(ERROR, str(error))

    def on_close(ws):
        addLogDetails(INFO, "Close")

    # Assign the callbacks.
    ss._on_open = on_open
    ss._on_message = on_message
    ss._on_error = on_error
    ss._on_close = on_close

    ss.connect()
    ss.run()


# @shared_task
# def createAngleOneCandle():
#     kolkata_tz=pytz.timezone('Asia/Kolkata')
#     task_id = current_task.request.id
#
#     # Create a job entry in the database
#     JobDetails.objects.create(
#         user_id=ADMIN_USER_ID,
#         index_name=SOCKET_JOB,
#         job_id=task_id,
#         strategy=SOCKET_JOB
#     )
#
#     # Fetch broker details for the admin user
#     user_broker_data = BrokerDetails.objects.filter(user_id=ADMIN_USER_ID, index_group=INDIAN_INDEX)
#     BrokerObject = AngelOneBroker(user_broker_data)
#
#     # Initialize WebSocket parameters
#     correlation_id = "admin_ws"
#     symbol_token = BrokerObject.getTokenForSymbol(BANKNIFTY_FUTURES)
#     tokens = [symbol_token]  # Define your tokens
#     print(tokens)
#     global start_time_dict
#     start_time_dict = {}
#     for tkn in tokens:
#         # started_time=get_next_minute_start()
#         # given_timestamp_millis=1725853100000
#         given_timestamp_millis =get_next_minute_start()
#         # print(given_timestamp_millis)
#         timestamp_seconds = given_timestamp_millis / 1000
#         # kolkata_tz = pytz.timezone('Asia/Kolkata')
#         # dt_utc = datetime.fromtimestamp(timestamp_seconds, pytz.utc)
#         # dt_kolkata = dt_utc.astimezone(kolkata_tz)
#
#         # Step 3: Convert to UTC datetime
#         dt_utc = datetime.datetime.fromtimestamp(timestamp_seconds, pytz.utc)
#
#         # Step 4: Convert to Asia/Kolkata timezone
#         kolkata_tz = pytz.timezone('Asia/Kolkata')
#         dt_kolkata = dt_utc.astimezone(kolkata_tz)
#
#         # print("UTC Time:", dt_utc)
#         # print("Kolkata Time:", dt_kolkata)
#         # nine_fifteen_am = kolkata_tz.localize(datetime(dt_kolkata.year, dt_kolkata.month, dt_kolkata.day, 9, 16))
#         # print(nine_fifteen_am)
#         # if dt_kolkata > nine_fifteen_am:
#         #     result = dt_kolkata
#         # else:
#         #     result = nine_fifteen_am
#         # Localize fixed 9:16 AM time on the same date
#         nine_fifteen_am = kolkata_tz.localize(
#             datetime.datetime(dt_kolkata.year, dt_kolkata.month, dt_kolkata.day, 9, 16))
#
#         print("9:16 AM:", nine_fifteen_am)
#         print("dt_kolkata:", dt_kolkata)
#
#         # Compare the datetime
#         if dt_kolkata > nine_fifteen_am:
#             result = dt_kolkata
#         else:
#             result = nine_fifteen_am
#
#         print("Result:", result)
#
#         result_timestamp = int(result.timestamp() * 1000)
#         print("Resulting datetime:", result_timestamp)
#         start_time_dict[tkn] = result_timestamp
#         print(start_time_dict)
#
#
#     def createWebSocketObj(token, exchangeType):
#         global mode
#         global token_list
#         action = 1
#         mode = 1
#
#         token_list = [
#             {
#                 "exchangeType": exchangeType,
#                 "tokens": token
#             }
#         ]
#         swsObj = SmartWebSocketV2(BrokerObject.auth_token, BrokerObject.broker_api_token, BrokerObject.broker_user_id,
#                                   BrokerObject.feed_token, max_retry_attempt=2)
#         return swsObj
#
#     sws = None
#
#     def on_open(wsapp):
#         global token_list
#         addLogDetails(INFO, "WebSocket connection opened")
#         # sws.subscribe(correlation_id, 1, [{"exchangeType": 2, "tokens": tokens}])
#         sws.subscribe(correlation_id, 1, token_list)
#
#     def on_data(wsapp, message):
#         try:
#             token = message['token']
#             ltp = message['last_traded_price'] / 100.0  # Ensure LTP is a float
#             data = {'token': token, 'ltp': ltp}
#             print(data)
#             for token in tokens:
#                 candle_current_time=datetime.datetime.now(kolkata_tz)
#                 if  candle_current_time.timestamp() * 1000 >= start_time_dict[token] :
#                     addLogDetails(INFO,"candle_current_time >= started time")
#                     from_time = get_previous_minute_start(start_time_dict[token],False)
#                     to_time = format_time_in_min(start_time_dict[token])
#                     candle_data_df = BrokerObject.getCandleData(NFO, token, from_time, to_time, "ONE_MINUTE")
#                     addLogDetails(INFO,candle_data_df)
#                     open_price = float(candle_data_df.loc[0, OPEN])
#                     high_price =float(candle_data_df.loc[0, HIGH])
#                     low_price = float(candle_data_df.loc[0, LOW])
#                     close_price = float(candle_data_df.loc[0, CLOSE])
#                     candle_time=candle_data_df.loc[0, CANDLE_TIMESTAMP]
#                     candle_time = pd.to_datetime(candle_time)
#                     candle_time = candle_time.strftime('%Y-%m-%d %H:%M:%S')
#                     candle_data = {"token": token, "time": candle_time, "open": open_price,
#                                    "high": high_price, "low": low_price, "close": close_price}
#                     update_candle_data_to_table(candle_data)
#                     addLogDetails(INFO,candle_data)
#                     start_time_dict[token] = get_next_minute_start()
#             update_ltp_to_table(data)
#         except Exception as e:
#             print(e)
#     def on_error(wsapp, error):
#         addLogDetails(ERROR, str(error))
#
#     def on_close(wsapp):
#         addLogDetails(INFO, "WebSocket connection closed")
#
#     def close_connection():
#         sws.close_connection()
#         addLogDetails(INFO, "WebSocket connection closed manually")
#
#     sws = createWebSocketObj(tokens, 2)
#     sws.on_open = on_open
#     sws.on_data = on_data
#     sws.on_error = on_error
#     sws.on_close = on_close
#
#     sws.connect()
#
#     def on_error(wsapp, error):
#         # Handle WebSocket errors
#         addLogDetails(ERROR, str(error))
#
#     def on_close(wsapp):
#         # Handle WebSocket closing
#         addLogDetails(INFO, "WebSocket connection closed")
#
#     def close_connection():
#         # Close WebSocket connection
#         sws.close_connection()
#         addLogDetails(INFO, "WebSocket connection closed manually")
#
#     # Create and configure the WebSocket
#     sws = createWebSocketObj([35165], 2)
#     sws.on_open = on_open
#     sws.on_data = on_data
#     sws.on_error = on_error
#     sws.on_close = on_close
#
#     # Connect to the WebSocket
#     sws.connect()


@shared_task()
def createAngleOneCandle():
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    task_id = current_task.request.id

    # Create Job Entry
    JobDetails.objects.create(
        user_id=ADMIN_USER_ID,
        index_name=SOCKET_JOB,
        job_id=task_id,
        strategy=SOCKET_JOB
    )

    try:
        user_broker_data = BrokerDetails.objects.filter(
            user_id=ADMIN_USER_ID, index_group=INDIAN_INDEX
        )
        BrokerObject = AngelOneBroker(user_broker_data)

        correlation_id = "admin_ws"
        index_names_for_candle = ['bank_nifty_fut']
        index_names_ltp_only = ['nifty', 'bank_nifty', 'fin_nifty']
        all_index_names = index_names_for_candle + index_names_ltp_only

        all_index_data = IndexDetails.objects.filter(index_name__in=all_index_names)

        tokens_for_candle = []
        tokens_ltp_only = []
        token_expiry_map = {}

        for entry in all_index_data:
            token = str(entry.index_token)
            token_expiry_map[token] = entry.current_expiry
            if entry.index_name in index_names_for_candle:
                tokens_for_candle.append(token)
            elif entry.index_name in index_names_ltp_only:
                tokens_ltp_only.append(token)

        all_tokens = tokens_for_candle + tokens_ltp_only
        #{"exchangeType": 1, "tokens": ['26000', '26009', '26037']},
        all_token_list = [
            
            {"exchangeType": 2, "tokens": tokens_for_candle}
        ]
        # all_token_list = [{"exchangeType": 2, "tokens": all_tokens}]
        print(all_token_list)

        # Build start_time_dict
        start_time_dict = {}
        for token in all_tokens:
            given_timestamp_millis = get_next_minute_start()
            timestamp_seconds = given_timestamp_millis / 1000
            dt_utc = datetime.datetime.fromtimestamp(timestamp_seconds, pytz.utc)
            dt_kolkata = dt_utc.astimezone(kolkata_tz)

            nine_fifteen = datetime.datetime(
                dt_kolkata.year, dt_kolkata.month, dt_kolkata.day, 9, 16, tzinfo=kolkata_tz
            )
            result_timestamp = int(max(dt_kolkata, nine_fifteen).timestamp() * 1000)
            start_time_dict[token] = result_timestamp

        # Callback creators
        def on_open(wsapp):
            addLogDetails(INFO, f"[WebSocket] Connection opened. Subscribing to tokens: {all_token_list}")
            sws.subscribe(correlation_id, 1, all_token_list)

        def on_data(wsapp, message):
            try:
                token = message['token']
                ltp = message['last_traded_price'] / 100.0
                # print({'token': token, 'ltp': ltp})
                update_ltp_to_table({'token': token, 'ltp': ltp})

                if token in tokens_for_candle:
                    now = datetime.datetime.now(kolkata_tz)
                    now_ts = int(now.timestamp() * 1000)

                    if now_ts >= start_time_dict[token]:
                        from_time = get_previous_minute_start(start_time_dict[token], False)
                        to_time = format_time_in_min(start_time_dict[token])

                        candle_df = BrokerObject.getCandleData(NFO, token, from_time, to_time, "ONE_MINUTE")
                        if candle_df.empty:
                            addLogDetails(INFO, f"No candle data for token {token} at {from_time} -> {to_time}")
                            return

                        candle_row = candle_df.iloc[0]
                        candle_data = {
                            "token": token,
                            "time": pd.to_datetime(candle_row[CANDLE_TIMESTAMP]).strftime('%Y-%m-%d %H:%M:%S'),
                            "open": float(candle_row[OPEN]),
                            "high": float(candle_row[HIGH]),
                            "low": float(candle_row[LOW]),
                            "close": float(candle_row[CLOSE])
                        }
                        update_candle_data_to_table(candle_data)
                        addLogDetails(INFO, f"[Candle Saved] {candle_data}")

                        start_time_dict[token] = get_next_minute_start()
            except Exception as e:
                addLogDetails(ERROR, f"[on_data] Error for token {message.get('token')}: {e}")

        def on_error(wsapp, error):
            addLogDetails(ERROR, f"[WebSocket] Error: {error}")

        def on_close(wsapp):
            addLogDetails(INFO, "[WebSocket] Connection closed.")

        # Create and connect WebSocket
        def create_websocket():
            ws = SmartWebSocketV2(
                BrokerObject.auth_token,
                BrokerObject.broker_api_token,
                BrokerObject.broker_user_id,
                BrokerObject.feed_token,
                max_retry_attempt=2
            )
            ws.on_open = on_open
            ws.on_data = on_data
            ws.on_error = on_error
            ws.on_close = on_close
            return ws

        MAX_RETRIES = 3
        RETRY_DELAY = 5  # seconds

        for attempt in range(MAX_RETRIES):
            try:
                sws = create_websocket()
                sws.connect()
                break
            except Exception as e:
                addLogDetails(ERROR, f"[Retry {attempt + 1}] WebSocket connection failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    addLogDetails(ERROR, "WebSocket failed after maximum retries.")

    except Exception as main_e:
        addLogDetails(ERROR, f"[Main Task Error] {main_e}")
    finally:
        JobDetails.objects.filter(job_id=task_id).update(
            status='completed', end_time=timezone.now()
        )




@shared_task
def angelOneWSNSE():
    task_id = current_task.request.id

    # Create a job entry in the database
    JobDetails.objects.create(
        user_id=ADMIN_USER_ID,
        index_name=SOCKET_JOB,
        job_id=task_id,
        strategy=SOCKET_JOB
    )

    # Fetch broker details for the admin user
    user_broker_data = BrokerDetails.objects.filter(user_id=ADMIN_USER_ID, index_group=INDIAN_INDEX)
    BrokerObject = AngelOneBroker(user_broker_data)

    # Initialize WebSocket parameters
    correlation_id = "admin_ws"
    nse_tokens = [99926000, 99926009, 99926037]  # Tokens for spot
    nfo_tokens = [BrokerObject.getTokenForSymbol(BANKNIFTY_FUTURES)]  # Tokens for futures


    global start_time_dict
    # ltp_values_dict = {}
    start_time_dict = {}

    def on_open(wsapp):
        addLogDetails(INFO, "WebSocket connection opened")
        new_token = [{"exchangeType": 1, "tokens": nse_tokens}, {"exchangeType": 2, "tokens": nfo_tokens}]
        sws.subscribe(correlation_id, 1, new_token)

    def on_data(wsapp, message):
        try:
            token = message['token']
            ltp = message['last_traded_price'] / 100.0  # Ensure LTP is a float
            data = {'token': token, 'ltp': ltp}
            print(data)
            update_ltp_to_table(data)
        except Exception as e:
            print(e)
            addLogDetails(ERROR, str(e))

    def on_error(wsapp, error):
        addLogDetails(ERROR, str(error))

    def on_close(wsapp):
        addLogDetails(INFO, "WebSocket connection closed")

    def close_connection():
        sws.close_connection()
        addLogDetails(INFO, "WebSocket connection closed manually")

    # Create and configure the WebSocket
    sws = SmartWebSocketV2(
            BrokerObject.auth_token,
            BrokerObject.broker_api_token,
            BrokerObject.broker_user_id,
            BrokerObject.feed_token,
            max_retry_attempt=2
        )
    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error
    sws.on_close = on_close

    # Connect to the WebSocket
    sws.connect()

    # Example usage of closing the connection (call close_connection when needed)
    # close_connection()



