import time
from SmartApi import SmartConnect, SmartWebSocket
import pyotp
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from celery import shared_task
from plutusAI.models import BrokerDetails, JobDetails
# from SmartApi import SmartWebSocket
from plutusAI.server.base import addLogDetails, update_ltp_to_table
from plutusAI.server.broker.AngelOneBroker import AngelOneBroker
from plutusAI.server.constants import *
# import SmartWebSocket
from celery import current_task


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
        swsObj = SmartWebSocketV2(BrokerObject.AUTH_TOKEN, BrokerObject.API_KEY, BrokerObject.CLIENT_CODE, BrokerObject.feed_token, max_retry_attempt=10)
        return swsObj

    sws = None

    def on_data(wsapp, message):
        data = {'token': message['token'], 'ltp': str(message['last_traded_price'] / 100)}
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
    addLogDetails(INFO,"Expiry Details updated from createHttpData")
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
