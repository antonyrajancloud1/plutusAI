from SmartApi import SmartConnect
import pandas as pd
import pyotp
import requests

from plutusAI.models import UserAuthTokens
from plutusAI.server.base import addLogDetails, getTokenUsingSymbol
from plutusAI.server.broker.AngelOne.AngelOneAuth import AngelOneAuth
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
            self.is_demo_enabled = bool(user_broker_details[IS_DEMO_TRADING_ENABLED])

            self.setUserTokenData()
            if self.user_token_data_list.__len__() > 0:
                addLogDetails(INFO,"into Existing token flow " +self.user_id)
                # self.user_token_data = self.user_token_data[0]
                self.initBrokerWithToken()
                profile_details = self.checkProfile()
                if profile_details[MESSAGE] == "SUCCESS":
                    addLogDetails(INFO,"Broker object initiated with existing token "+self.user_id)
                else:
                    # print("Generate token")
                    AngelOneAuth(self.user_id)
                    self.setUserTokenData()
                    self.initBrokerWithToken()
                    addLogDetails(INFO,"New Token generated "+ self.user_id)
            else:
                addLogDetails(INFO,"No Token Data "+ self.user_id)
                AngelOneAuth(self.user_id)
                self.setUserTokenData()
                self.initBrokerWithToken()
                addLogDetails(INFO,"New Token generated "+ self.user_id)
            # print(self.refreshToken)
            # print(self.auth_token)
            # print(self.feed_token)
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

    def setUserTokenData(self):
        self.user_token_data_query = UserAuthTokens.objects.filter(user_id=self.user_id)
        self.user_token_data_list = list(self.user_token_data_query.values())
        if self.user_token_data_list.__len__() > 0:
            self.user_token_data = self.user_token_data_list[0]

    def initBrokerWithToken(self):
        self.refreshToken = self.user_token_data["refreshToken"]
        self.feed_token = self.user_token_data["feedToken"]
        self.auth_token = self.user_token_data["jwtToken"]
        self.smartApi = SmartConnect(self.broker_api_token)
        self.smartApi.__init__(refresh_token=self.refreshToken,
                               feed_token=self.feed_token, access_token=self.auth_token,
                               api_key=self.broker_api_token)

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
        addLogDetails(INFO,order_details)
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
            addLogDetails(INFO,order_details)
            order_status = order_details['data']['status']
            if order_status.__eq__('trigger pending') or order_status.__eq__('open'):
                return True
            else:
                return False
        except Exception as e:
            addLogDetails(ERROR, "exception in checkIfOrderExists" + str(e))

    def getPrice(self, uniq_order_id):
        price_details = self.getOrderDetails(uniq_order_id)
        return str(price_details['averageprice'])

    def getCandleData(self, exchange, symbol, from_time, to_time,time_frame):
        try:
            column = ['timestamp', "open", "high", "low", "close", "volume"]
            dataParam = {
                "exchange": exchange,
                "symboltoken": symbol,
                "interval": time_frame,
                "fromdate": from_time,
                "todate": to_time
            }
            print(dataParam)
            historic_data = self.smartApi.getCandleData(dataParam)
            candle_data = historic_data["data"]
            if historic_data["message"] == "SUCCESS":
                df = pd.DataFrame(candle_data, columns=column)
                print(df)
                return df
        except Exception as e:
            addLogDetails(ERROR, "exception in getCandleData" + str(e))
            return GLOBAL_ERROR
