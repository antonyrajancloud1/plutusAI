import json
from concurrent.futures import ThreadPoolExecutor

import requests
from playwright.sync_api import sync_playwright
from plutusAI.models import UserAuthTokens, BrokerDetails, ManualOrders, OrderBook
from plutusAI.server.base import getCurrentTimestamp, addOrderBookDetails
import re

from plutusAI.server.constants import *
from threading import Lock



class ExnessBroker:
    LOGIN_URL = "https://my.exness.com/v4/wta-api/signin?captchaVersion=3"

    def __init__(self, user_id: str):
        self.access_token = None
        self.email = user_id
        user_token_data = UserAuthTokens.objects.filter(
            user_id=user_id, index_group="forex"
        )
        user_data = BrokerDetails.objects.filter(
            user_id=user_id, index_group="forex"
        )
        if len(list(user_data.values()))>0:
            user_broker_data=list(user_data.values())[0]
            self.password = user_broker_data["broker_password"]
            self.broker_user_id = user_broker_data["broker_user_id"]
            self.broker_forex_server = user_broker_data["broker_forex_server"]
            self.broker_user_name = user_broker_data["broker_user_name"]
        self.executor = ThreadPoolExecutor(max_workers=50)
        self.user_locks = {}

    def get_token(self) -> dict:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Change to True to hide browser
            context = browser.new_context()
            page = context.new_page()

            # Navigate to login page
            page.goto(self.LOGIN_URL)
            page.wait_for_timeout(5000)  # Let Cloudflare JS challenge complete

            # Perform login and get response
            response = page.evaluate(f"""async () => {{
                const res = await fetch("{self.LOGIN_URL}", {{
                    method: "POST",
                    headers: {{
                        "Content-Type": "application/json"
                    }},
                    body: JSON.stringify({{
                        login: "{self.broker_user_id}",
                        password: "{self.password}",
                        action: "LOGIN"
                    }})
                }});
                return await res.json();
            }}""")

            browser.close()
            return response

    def update_token_in_db(self):
        token_details = self.get_token()
        print(token_details)
        current_time_str = getCurrentTimestamp()

        # Validate expected keys
        if "token" not in token_details or "refresh" not in token_details or "user_uid" not in token_details:
            raise ValueError(f"Invalid token response: {token_details}")
        self.access_token = token_details["token"]
        user_token_data = {
            "feedToken": token_details["token"],
            "refreshToken": token_details["refresh"],
            "jwtToken": token_details["user_uid"],
            "last_updated_time": current_time_str,
            "user_id": self.email,
            "index_group":"forex"

        }

        user_data = UserAuthTokens.objects.filter(user_id=self.email, index_group="forex")
        if user_data.exists():
            user_data.update(**user_token_data)
        else:
            UserAuthTokens.objects.create(**user_token_data)

        return user_token_data


    def construct_server_path(self,server_str):
        print("Input:", server_str)
        match = re.search(r'MT(\d)([a-zA-Z]+)(\d+)', server_str, re.IGNORECASE)
        if match:
            platform = f"mt{match.group(1)}"  # e.g., mt5
            label = match.group(2).lower()  # e.g., trial
            number = match.group(3)  # e.g., 17
            return f"{platform}/{label}{number}"  # mt5/trial17
        return None

    def placeOrderForex(self, order_type, data_json):
        self.exitOrderForex(data_json)
        # Set default values
        instrument = data_json.get("ticker", "XAUUSD")+"m"
        price = float(data_json.get("price", 3360))
        sl = float(data_json.get("sl", 0))
        tp = float(data_json.get("tp", 0))
        user_strategy = data_json.get("strategy", "Forex_strategy")
        print(user_strategy)
        # Fetch user data
        user_data = UserAuthTokens.objects.filter(user_id=self.email, index_group="forex")
        user_manual_data = ManualOrders.objects.filter(user_id=self.email, index_group="forex")
        user_orderbook_data = OrderBook.objects.filter(user_id=self.email, index_group="forex", script_name=instrument,strategy=user_strategy,exit_price=None)
        print(user_orderbook_data)
        # Prevent duplicate orders
        if user_orderbook_data.exists():
            return ORDER_PRESENT

        # Get lot size from manual config or fallback
        user_lot_size = "0.01"
        if user_manual_data.exists():
            user_lot_size = str(getattr(user_manual_data.first(), "lots", "0.01"))

        # Get token
        if not user_data.exists():
            self.update_token_in_db()
            return

        user_data = user_data.first()
        print(user_data)
        # print(json.loads(user_data))
        self.access_token = user_data.feedToken
        print(self.access_token)
        # Construct order URL
        url = f"https://rtapi-sg.eccweb.mobi/rtapi/{self.construct_server_path(self.broker_forex_server)}/v1/accounts/{self.broker_user_name}/orders"
        print("URL:", url)

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = {
            "order": {
                "instrument": instrument,
                "price": price,
                "type": order_type,
                "volume": float(user_lot_size),
                "sl": sl,
                "tp": tp,
                "deviation": 0,
                "oneClick": True
            }
        }
        # Make the POST request
        self.response = requests.post(url, headers=headers, json=payload)
        print("Status:", self.response)

        # Retry if token expired
        if self.response.status_code == 401 or self.response.status_code == 400:
            self.update_token_in_db()
            print("Reposne BS 2")
            print(self.access_token)
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            self.response = requests.post(url, headers=headers, json=payload)
            print( self.response )

        try:
            self.res_json = self.response.json()
            print(self.res_json)
            order_id=self.res_json["order"]["order_id"]
            position_id = self.res_json["order"]["position_id"]
            # Log order in DB
            data = {
                USER_ID: self.email,
                SCRIPT_NAME: instrument,
                QTY: float(user_lot_size),
                ENTRY_PRICE: price,
                STATUS: ORDER_PLACED,
                STRATEGY: user_strategy,
                INDEX_NAME: instrument,
                INDEX_GROUP: "forex",
                "order_id":order_id,
                "position_id":position_id
            }
            print(data)
            addOrderBookDetails(data, True)
            return ORDER_PLACED

        except Exception as e:
            print(f"Failed to parse JSON response: {e}")
            return f"Failed to parse JSON response: {e}"



    def exitOrderForex(self, data_json):
        exit_data = {}
        exit_data[EXIT_TIME] = getCurrentTimestamp()
        # Set default values
        instrument = data_json.get("ticker", "XAUUSD")+"m"
        price = float(data_json.get("price", 3360))
        user_strategy = data_json.get("strategy", "Forex_strategy")
        user_orderbook_data = OrderBook.objects.filter(user_id=self.email, index_group="forex", script_name=instrument,
                                                       strategy=user_strategy,exit_price=None)
        user_data = UserAuthTokens.objects.filter(user_id=self.email, index_group="forex")
        user_manual_data = ManualOrders.objects.filter(user_id=self.email, index_group="forex")

        print(user_orderbook_data)
        # Prevent duplicate orders
        if user_orderbook_data.exists():
            user_position_id = str(getattr(user_orderbook_data.first(), "position_id"))
            url = f"https://rtapi-sg.eccweb.mobi/rtapi/{self.construct_server_path(self.broker_forex_server)}/v2/accounts/{self.broker_user_name}/positions/{user_position_id}/close"
            print("URL:", url)

            if not user_data.exists():
                self.update_token_in_db()
                return

            user_data = user_data.first()
            user_lot_size = "0.01"
            if user_manual_data.exists():
                user_lot_size = str(getattr(user_manual_data.first(), "lots", "0.01"))

            print(user_data)
            self.access_token = user_data.feedToken
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            payload = {"position":{"price":price,"volume":float(user_lot_size),"close_by_id":0}}

            # Make the POST request
            self.response = requests.put(url, headers=headers, json=payload)
            self.res_json = self.response.json()
            print(self.res_json)
            if self.response.status_code == 401 or self.response.status_code == 400:
                self.update_token_in_db()
                self.response = requests.put(url, headers=headers, json=payload)
                print("Reponse 2")
                print(self.response.json())
            exit_price = self.res_json["position"]["price"]
            order_info = user_orderbook_data.values().first()
            entry_price = order_info.get(ENTRY_PRICE)
            exit_data.update({
                TOTAL: str((float(exit_price) - float(entry_price)) * float(user_lot_size)),
                EXIT_PRICE: exit_price,
                STATUS: ORDER_EXITED
            })
            user_orderbook_data.update(**exit_data)
            addOrderBookDetails(exit_data, False)
            return "Order Exited"
        else:
            return "No Orders Present"



    def get_user_lock(self,user_email, strategy):
        key = f"{user_email}_{strategy}"
        if key not in self.user_locks:
           self.user_locks[key] = Lock()
        return self.user_locks[key]

    def submit_exitOrderForex(self, data_json):
        # self.exitOrderForex(self, data_json)
        self.executor.submit(self.exitOrderForex, data_json)

    def submit_placeOrderForex(self, order_type, data_json):
        # self.placeOrderForex(self, order_type, data_json)
        self.executor.submit(self.placeOrderForex, order_type, data_json)
        return "Order placed"