from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from celery import current_task

from plutusAI.server.base import *
from plutusAI.server.constants import *
from plutusAI.server.broker.Broker import Broker

class WebsocketAngelOne:

    def __init__(self, user_email, index_name, symbol_token, strategy):
        print(user_email)
        print(symbol_token)
        # self.task_id = current_task.request.id
        self.correlation_id = "admin_ws"
        # self.sws = None
        self.user_email = user_email
        self.index_name = index_name
        self.strategy = strategy
        # Initialize the broker object and tokens
        # self.user_broker_data = BrokerDetails.objects.filter(user_id=user_email, index_group=INDIAN_INDEX)
        self.BrokerObject = Broker(self.user_email,INDIAN_INDEX).BrokerObject
        self.symbol_token = symbol_token

        # self.create_job_entry()
        self.connectWS()
    def create_job_entry(self):
        JobDetails.objects.create(
            user_id=self.user_email,
            index_name=self.index_name,
            job_id=self.task_id,
            strategy=self.strategy
        )

    def create_websocket_obj(self, token, exchangeType):
        print(token)
        self.token_list = [
            {
                "exchangeType": exchangeType,
                "tokens": token
            }
        ]
        swsObj = SmartWebSocketV2(
            self.BrokerObject.auth_token,
            self.BrokerObject.broker_api_token,
            self.BrokerObject.broker_user_id,
            self.BrokerObject.feed_token,
            max_retry_attempt=2
        )
        return swsObj

    def on_open(self, wsapp):
        addLogDetails(INFO, "WebSocket connection opened")
        self.sws.subscribe(self.correlation_id, 1, self.token_list)

    def on_data(self, wsapp, message):
        try:
            token = message['token']
            ltp = message['last_traded_price'] / 100.0  # Ensure LTP is a float
            data = {'token': token, 'ltp': ltp}
            print(data)

        except Exception as e:
            print(e)

    def on_error(self, wsapp, error):
        addLogDetails(ERROR, str(error))

    def on_close(self, wsapp):
        addLogDetails(INFO, "WebSocket connection closed")

    def close_connection(self):
        self.sws.close_connection()
        addLogDetails(INFO, "WebSocket connection closed manually")

    def connectWS(self):
        print("connectWSconnectWS")
        print(self.symbol_token )
        self.sws = self.create_websocket_obj(self.symbol_token , 2)
        self.sws.on_open = self.on_open
        self.sws.on_data = self.on_data
        self.sws.on_error = self.on_error
        self.sws.on_close = self.on_close
        self.sws.connect()

