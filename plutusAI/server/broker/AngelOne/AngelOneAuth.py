import http.client
import json
import mimetypes
import requests

import pyotp

from plutusAI.models import BrokerDetails, UserAuthTokens
from plutusAI.server.base import *
from plutusAI.server.constants import *


class AngelOneAuth:
    def __init__(self, user_email):
        self.user_broker_data = BrokerDetails.objects.filter(user_id=user_email, index_group=INDIAN_INDEX)
        self.user_broker_details = list(self.user_broker_data.values())
        if len(self.user_broker_details) > 0:
            self.user_broker_details = self.user_broker_details[0]
            self.user_id = self.user_broker_details[USER_ID]
            self.broker_user_id = self.user_broker_details[BROKER_USER_ID]
            self.broker_mpin = self.user_broker_details[BROKER_MPIN]
            self.broker_qr = self.user_broker_details[BROKER_QR]
            self.broker_api_token = self.user_broker_details[BROKER_API_TOKEN]
            self.totp = pyotp.TOTP(self.broker_qr).now()
            addLogDetails(INFO, "user_broker_details")
            addLogDetails(INFO, self.user_broker_details)
            self.GenerateAuthToken()
        else:
            no_broker_data = "No Broker Details Present for Email : " + self.user_id
            print(no_broker_data)
            addLogDetails(ERROR, no_broker_data)

    # def GenerateAuthToken(self):
    #     try:
    #         addLogDetails(INFO, "Into GenerateAuthToken")
    #         conn = http.client.HTTPSConnection(
    #             "apiconnect.angelbroking.com"
    #         )
    #         # payload = "{\n\"clientcode\":\"A58033497\",\n\"password\":\"1005\"\n,\n\"totp\":\"482435\"\n}"
    #         payload = "{\n\"clientcode\":\"" + self.broker_user_id + "\",\n\"password\":\"" + self.broker_mpin + "\"\n,\n\"totp\":\"" + self.totp + "\"\n}"
    #         headers = {
    #             'Content-Type': 'application/json',
    #             'Accept': 'application/json',
    #             'X-UserType': 'USER',
    #             'X-SourceID': 'WEB',
    #             'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
    #             'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
    #             'X-MACAddress': 'MAC_ADDRESS',
    #             'X-PrivateKey': self.broker_api_token
    #         }
    #         conn.request(
    #             "POST",
    #             "/rest/auth/angelbroking/user/v1/loginByPassword", payload, headers)

    #         res = conn.getresponse()
    #         data = res.read()
    #         # print(data.decode("utf-8"))
    #         addLogDetails(INFO, json.loads(data.decode("utf-8")))
    #         self.updateUserToken(json.loads(data.decode("utf-8")))
    #     except Exception as e:
    #         addLogDetails(ERROR, e)
    def GenerateAuthToken(self):
        try:
            addLogDetails(INFO, "Into GenerateAuthToken")

            url = "https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByPassword"
            payload = {
                "clientcode": self.broker_user_id,
                "password": self.broker_mpin,
                "totp": self.totp
            }
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-UserType': 'USER',
                'X-SourceID': 'WEB',
                'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
                'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
                'X-MACAddress': 'MAC_ADDRESS',
                'X-PrivateKey': self.broker_api_token
            }

            response = requests.post(url, json=payload, headers=headers)
            addLogDetails(INFO, f"API Response: {response.json()}")

            if response.status_code == 200:
                self.updateUserToken(response.json())
            else:
                addLogDetails(ERROR, f"API request failed with status code {response.status_code}")

        except Exception as e:
            addLogDetails(ERROR, f"Error during API request: {str(e)}")

    def updateUserToken(self, token_data):
        try:
            current_time_str = getCurrentTimestamp()
            # print(token_data)
            if token_data["message"] == "SUCCESS":
                user_token_data = token_data["data"]
                user_token_data["last_updated_time"] = current_time_str
                user_token_data["user_id"] = self.user_id
                del user_token_data["state"]
                # print(user_token_data)
                user_data = UserAuthTokens.objects.filter(
                    user_id=self.user_id
                )

                if list(user_data.values()).__len__() > 0:
                    user_data.update(**user_token_data)
                else:
                    UserAuthTokens.objects.create(**user_token_data)
            else:
                print("No data")

        except Exception as e:
            addLogDetails(ERROR, "error in updateUserToken " + str(e))
