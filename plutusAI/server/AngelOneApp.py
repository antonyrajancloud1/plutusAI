import datetime
import time
from SmartApi import SmartConnect, SmartWebSocket
import pyotp
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from celery import shared_task
from plutusAI.models import BrokerDetails, JobDetails, CandleData
# from SmartApi import SmartWebSocket
from plutusAI.server.base import addLogDetails, update_ltp_to_table, get_next_minute_start, format_time, \
    update_candle_data_to_table
from plutusAI.server.broker.AngelOneBroker import AngelOneBroker
from plutusAI.server.constants import *
# import SmartWebSocket
from celery import current_task
import pandas as pd

from plutusAI.server.websocket.WebsocketAngelOne import OHLCDataProcessor


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
        index_name=SOCKET_JOB,
        job_id=task_id,
        strategy=SOCKET_JOB
    )
    user_broker_data = BrokerDetails.objects.filter(user_id=ADMIN_USER_ID, index_group=INDIAN_INDEX)
    BrokerObject = AngelOneBroker(user_broker_data)
    allData = []
    niftyData = BrokerObject.getCurrentPremiumDetails(NSE, NIFTY_50)  # "Nifty 50"
    BNData = BrokerObject.getCurrentPremiumDetails(NSE, NIFTY_BANK)
    FNData = BrokerObject.getCurrentPremiumDetails(NSE, NIFTY_FIN_SERVICE)
    allData.append(niftyData)
    allData.append(BNData)
    allData.append(FNData)
    addLogDetails(INFO, "Expiry Details updated from createHttpData")
    while True:
        for data in allData:
            value = {TOKEN: data[SYMBOL_TOKEN], LTP: str(BrokerObject.getLtpForPremium(data))}
            if value[LTP] != None:
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
        addLogDetails("Ticks: {}".format(message))

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


@shared_task
def createAngleOneCandle():
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
    # tokens = [99926000, 99926009]
    tokens=[35165]
    global ltp_values_dict
    global candlestick_data_dict
    global start_time_dict
    candlestick_data_dict = {}
    ltp_values_dict = {}
    start_time_dict = {}
    for tkn in tokens:
        candlestick_data_dict[tkn] = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close'])
        ltp_values_dict[tkn] = []
        start_time_dict[tkn] = get_next_minute_start()

    def createWebSocketObj(token, exchangeType):
        # Create a SmartWebSocketV2 object with the given token and exchange type
        mode = 1
        token_list = [{"exchangeType": exchangeType, "tokens": token}]
        swsObj = SmartWebSocketV2(BrokerObject.auth_token, BrokerObject.broker_api_token, BrokerObject.broker_user_id,
                                  BrokerObject.feed_token, max_retry_attempt=2)
        return swsObj


    def on_open(wsapp):

        # Handle WebSocket opening
        addLogDetails(INFO, "WebSocket connection opened")
        sws.subscribe(correlation_id, 1, [{"exchangeType": 2, "tokens": tokens}])


    def on_data(wsapp, message):
        token = message['token']
        ltp = str(message['last_traded_price'] / 100)
        # Handle incoming data from the WebSocket
        data = {'token': token, 'ltp': ltp}
        # print(data)
        # time.sleep(1)

        for token in tokens:
            value = data
            print(value)
            ltp = value[LTP]

            if value[LTP] is not None:
                # update_ltp_to_table(value)
                print(ltp_values_dict[token])

                ltp = float(ltp)
                ltp_values_dict[token].append(ltp)

                if datetime.datetime.now() >= start_time_dict[token] + datetime.timedelta(seconds=60):
                    # Calculate OHLC values
                    open_price = ltp_values_dict[token][0]
                    high_price = max(ltp_values_dict[token])
                    low_price = min(ltp_values_dict[token])
                    close_price = ltp_values_dict[token][-1]

                    # Print OHLC values and current time
                    print(
                        f"{format_time(start_time_dict[token])} - Token: {token}, Open: {open_price}, High: {high_price}, Low: {low_price}, Close: {close_price}")
                    candle_data = {"token":token,"time":format_time(start_time_dict[token]),"open":open_price,"high":high_price,"low":low_price,"close":close_price}
                    # Create a new row of data
                    # new_data = pd.DataFrame({
                    #     'timestamp': [start_time_dict[token]],
                    #     'open': [open_price],
                    #     'high': [high_price],
                    #     'low': [low_price],
                    #     'close': [close_price]
                    # })
                    update_candle_data_to_table(candle_data)
                    print("candle data pushed")
                    # Concatenate the new data with the existing candlestick_data for the token
                    # candlestick_data_dict[token] = pd.concat([candlestick_data_dict[token], new_data],
                    #                                          ignore_index=True)

                    # Clear the list for the next 60 seconds
                    ltp_values_dict[token] = []

                    # Update start time for the next 60-second interval for the specific token
                    start_time_dict[token] = get_next_minute_start()

        update_ltp_to_table(data)


    def on_error(wsapp, error):
        # Handle WebSocket errors
        addLogDetails(ERROR, str(error))

    def on_close(wsapp):
        # Handle WebSocket closing
        addLogDetails(INFO, "WebSocket connection closed")

    def close_connection():
        # Close WebSocket connection
        sws.close_connection()
        addLogDetails(INFO, "WebSocket connection closed manually")

    # Create and configure the WebSocket
    sws = createWebSocketObj(tokens, 2)
    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error
    sws.on_close = on_close

    # Connect to the WebSocket
    sws.connect()


@shared_task
def createHttpDataCandels():
    task_id = current_task.request.id
    print(task_id)
    JobDetails.objects.create(
        user_id=ADMIN_USER_ID,
        index_name=SOCKET_JOB,
        job_id=task_id,
        strategy=SOCKET_JOB
    )
    print("job created")
    user_broker_data = BrokerDetails.objects.filter(user_id=ADMIN_USER_ID, index_group=INDIAN_INDEX)
    BrokerObject = AngelOneBroker(user_broker_data)
    allData = []
    niftyData = BrokerObject.getCurrentPremiumDetails(NSE, NIFTY_50)  # "Nifty 50"
    BNData = BrokerObject.getCurrentPremiumDetails(NSE, NIFTY_BANK)
    FNData = BrokerObject.getCurrentPremiumDetails(NSE, NIFTY_FIN_SERVICE)
    BN_FUT = BrokerObject.getCurrentPremiumDetails(NFO, BANKNIFTY_FUTURES)
    allData.append(niftyData)
    allData.append(BNData)
    allData.append(FNData)
    allData.append(BN_FUT)
    addLogDetails(INFO, "Expiry Details updated from createHttpData")
    def getAllTokens():
        token=[]
        for data in allData:
            token.append(data[SYMBOL_TOKEN])
        return token
    candlestick_data_dict = {}
    ltp_values_dict = {}
    start_time_dict = {}
    tokens = getAllTokens()
    print(tokens)
    try:
        for tkn in tokens:
            candlestick_data_dict[tkn] = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close'])
            ltp_values_dict[tkn] = []
            start_time_dict[tkn] = get_next_minute_start()
        while True:
            time.sleep(1)
            for data in allData:
                value = {TOKEN: data[SYMBOL_TOKEN], LTP: str(BrokerObject.getLtpForPremium(data))}
                token = data[SYMBOL_TOKEN]
                ltp = value[LTP]

                if value[LTP] is not None:
                    update_ltp_to_table(value)
                    print(ltp_values_dict[token])

                    ltp = float(ltp)
                    ltp_values_dict[token].append(ltp)

                    if datetime.datetime.now() >= start_time_dict[token] + datetime.timedelta(seconds=60):
                        # Calculate OHLC values
                        open_price = ltp_values_dict[token][0]
                        high_price = max(ltp_values_dict[token])
                        low_price = min(ltp_values_dict[token])
                        close_price = ltp_values_dict[token][-1]

                        # Print OHLC values and current time
                        print(
                            f"{format_time(start_time_dict[token])} - Token: {token}, Open: {open_price}, High: {high_price}, Low: {low_price}, Close: {close_price}")
                        # data = {"token":token,"index_name":data[TRADING_SYMBOL],"time":format_time(start_time_dict[token]),"open":open_price,"high":high_price,"low":low_price,"close":close_price}
                        # Create a new row of data
                        new_data = pd.DataFrame({
                            'timestamp': [start_time_dict[token]],
                            'open': [open_price],
                            'high': [high_price],
                            'low': [low_price],
                            'close': [close_price]
                        })
                        CandleData.objects.create(
                            index_name=data[TRADING_SYMBOL],
                            token=token,
                            time=format_time(start_time_dict[token]),
                                open=open_price,
                                high=high_price,
                                low=low_price,
                                close=close_price
                            )
                        # Concatenate the new data with the existing candlestick_data for the token
                        candlestick_data_dict[token] = pd.concat([candlestick_data_dict[token], new_data],
                                                                 ignore_index=True)

                        # Clear the list for the next 60 seconds
                        ltp_values_dict[token] = []

                        # Update start time for the next 60-second interval for the specific token
                        start_time_dict[token] = get_next_minute_start()

                        # Wait for the next iteration
                    # time.sleep(.5)

    except Exception as e:
        print(e)
