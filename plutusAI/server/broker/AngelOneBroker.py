from SmartApi import SmartConnect
import pandas as pd
import pyotp
import requests
from plutusAI.server.base import addLogDetails, getTokenUsingSymbol
from plutusAI.server.constants import *


class AngelOneBroker:
    def __init__(self, user_broker_data):
        try:

            user_broker_details = list(user_broker_data.values())[0]
            self.user_id = user_broker_details[USER_ID]
            self.broker_user_id = user_broker_details[BROKER_USER_ID]
            self.broker_api_token = user_broker_details[BROKER_API_TOKEN]
            self.broker_mpin = user_broker_details[BROKER_MPIN]
            self.broker_qr = user_broker_details[BROKER_QR]
            self.smartApi = SmartConnect(self.broker_api_token)
            self.totp = pyotp.TOTP(self.broker_qr).now()
            self.data = self.smartApi.generateSession(self.broker_user_id, self.broker_mpin, self.totp)
            self.refreshToken = self.data['data']['refreshToken']
            self.auth_token = self.data['data']['jwtToken']
            self.feed_token = self.data['data']['feedToken']
            self.profileDetails = self.checkProfile()
            # print(self.profileDetails)
            if str(self.profileDetails["message"]).__eq__("SUCCESS"):
                data = {"token_status": "generated", BROKER_USER_NAME: self.profileDetails["data"]["name"]}
                user_broker_data.update(**data)

            self.headers = {"Authorization": "Bearer " + self.auth_token}
            self.session = requests.session()
            self.root_url = 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1'
            self.margin_url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
            self.df = pd.DataFrame.from_dict(requests.get(self.margin_url).json())
            addLogDetails(INFO, "initisuccess for angleone")
        except Exception as e:
            addLogDetails(ERROR, str(e))

    def checkProfile(self):
        return self.smartApi.getProfile(self.refreshToken)

    def getTokenForSymbol(self, symbol):
        try:
            df = self.df
            df = df[(df.symbol == symbol)]
            # print(df)
            token = df.iloc[0]['token']
            return token
        except Exception as e:
            addLogDetails(ERROR, str(e))

    def getCurrentAtm(self, index_name):
        try:
            # print(index_name)
            match index_name:
                case "nifty":
                    indexValue = 50
                    index_ltp = self.smartApi.ltpData("NSE", index_name, "99926000")["data"]['ltp']
                    # print(index_ltp)
                    index_spot = indexValue * round(index_ltp / indexValue)
                    return index_spot
                case "bank_nifty":
                    indexValue = 100
                    index_ltp = self.smartApi.ltpData("NSE", index_name, "99926009")["data"]['ltp']
                    # print(index_ltp)
                    index_spot = indexValue * round(index_ltp / indexValue)
                    return index_spot
                case "fin_nifty":
                    indexValue = 50
                    index_ltp = self.smartApi.ltpData("NSE", index_name, "99926037")["data"]['ltp']
                    # print(index_ltp)
                    index_spot = indexValue * round(index_ltp / indexValue)
                    return index_spot
        except Exception as e:
            addLogDetails(ERROR, "Error in getCurrentAtm " + str(e))

    def placeOrder(self, order_details):
        orderid = self.smartApi.placeOrderFullResponse(order_details)
        return orderid

    def getOrderDetails(self, unique_order_id):
        order_details = self.smartApi.individual_order_details(unique_order_id)
        # print("getOrderDetails")
        # print(order_details)
        return order_details['data']

    def getCurrentPremiumDetails(self, exchange, currentPremiumPlaced):
        token = self.getTokenForSymbol(currentPremiumPlaced)
        optionDetails = {EXCHANGE: exchange, TRADING_SYMBOL: currentPremiumPlaced, SYMBOL_TOKEN: token}
        return optionDetails

    def getLtpForPremium(self, optionDetails):
        try:
            # print(optionDetails)
            ltpInfo = self.smartApi.ltpData(optionDetails[EXCHANGE], optionDetails[TRADING_SYMBOL],
                                            optionDetails[SYMBOL_TOKEN])
            data = str(ltpInfo['data']['ltp'])
            # print(data)
            return data
        except Exception as e:
            # print("exception in getltpForPremium")
            addLogDetails(ERROR, "exception in getltpForPremium " + str(e))
            return CONNECTION_ERROR

    def modifyOrder(self, order_details):
        try:
            orderid = self.smartApi.modifyOrder(order_details)
            return orderid
        except Exception as e:
            # print("exception in modifyOrder")
            addLogDetails(ERROR, "exception in modifyOrder" + str(e))

    def checkIfOrderExists(self, order_details):
        try:
            order_details = self.smartApi.individual_order_details(order_details)
            # print(order_details)
            order_status = order_details['data']['status']
            if order_status.__eq__('trigger pending'):
                return True
            else:
                return False
        except Exception as e:
            addLogDetails(ERROR, "exception in checkIfOrderExists" + str(e))

    def getPrice(self, uniq_order_id):
        price_details = self.getOrderDetails(uniq_order_id)
        return str(price_details['averageprice'])
