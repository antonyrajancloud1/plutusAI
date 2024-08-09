from datetime import datetime

from SmartApi import SmartConnect
from celery.result import AsyncResult
import time
from django.http import JsonResponse
from plutusAI.models import BrokerDetails, UserAuthTokens
from plutusAI.server.base import addLogDetails, getTokenUsingSymbol, getTradingSymbol, current_time
from plutusAI.server.broker.AngelOne.AngelOneAuth import AngelOneAuth
from plutusAI.server.broker.AngelOneBroker import AngelOneBroker
from plutusAI.server.constants import *


def testerCheck(request):
    # refreshToken = "eyJhbGciOiJIUzUxMiJ9.eyJ0b2tlbiI6IlJFRlJFU0gtVE9LRU4iLCJSRUZSRVNILVRPS0VOIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5WDNSNWNHVWlPaUpqYkdsbGJuUWlMQ0owYjJ0bGJsOTBlWEJsSWpvaWRISmhaR1ZmY21WbWNtVnphRjkwYjJ0bGJpSXNJbWR0WDJsa0lqb3dMQ0prWlhacFkyVmZhV1FpT2lJNE9UZ3lObU14TWkxaU1EaGtMVE0yTVRVdE9UTTVZaTFpTXpWbE56SmhOMlUzTUdNaUxDSnJhV1FpT2lKMGNtRmtaVjlyWlhsZmRqRWlMQ0p2Ylc1bGJXRnVZV2RsY21sa0lqb3dMQ0pwYzNNaU9pSnNiMmRwYmw5elpYSjJhV05sSWl3aWMzVmlJam9pUVRVNE1ETXpORGszSWl3aVpYaHdJam94TnpJek1qSXdOamsyTENKdVltWWlPakUzTWpNd05EYzRNellzSW1saGRDSTZNVGN5TXpBME56Z3pOaXdpYW5ScElqb2lObVF5WkdNMk16WXRaV1E0TlMwME9UazBMV0ptWWpVdFltUTBaR1pqTWpNM016RXpJbjAuWDF1Rl9wdmpVTHlnaml0VEVCRW9FZGVVR2V3TVJVLW53QjU2VDVIOEx2YkNNVEhCanMwdUxmSkdpUnRyUVp0b284NDBhS1JETDhVWlA2SFZJa2lQY0lRbVJxOWRMS0JLTnRSRmo2NHYtZnVlV3JrNnNjU2loVFJMSjkwN2w3Q0tEeWRFSDRyek1mZjJmQmIxbG9UeThiVDNoUWFQRUF3MkY5QUl1aWJFNWdjIiwiaWF0IjoxNzIzMDQ3ODk2fQ.EHbDDCcr8pnAO4ANdFh_QLjYSAfpxdWyVMk-PbVjq_IwFVTaSW6rdYxlr2XN1IHMaNSV2XmFn9DsAVGnvqxnbQ"
    # auth_token = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IkE1ODAzMzQ5NyIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKU1V6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUoxYzJWeVgzUjVjR1VpT2lKamJHbGxiblFpTENKMGIydGxibDkwZVhCbElqb2lkSEpoWkdWZllXTmpaWE56WDNSdmEyVnVJaXdpWjIxZmFXUWlPakVzSW5OdmRYSmpaU0k2SWpNaUxDSmtaWFpwWTJWZmFXUWlPaUk0T1RneU5tTXhNaTFpTURoa0xUTTJNVFV0T1RNNVlpMWlNelZsTnpKaE4yVTNNR01pTENKcmFXUWlPaUowY21Ga1pWOXJaWGxmZGpFaUxDSnZiVzVsYldGdVlXZGxjbWxrSWpveExDSndjbTlrZFdOMGN5STZleUprWlcxaGRDSTZleUp6ZEdGMGRYTWlPaUpoWTNScGRtVWlmWDBzSW1semN5STZJblJ5WVdSbFgyeHZaMmx1WDNObGNuWnBZMlVpTENKemRXSWlPaUpCTlRnd016TTBPVGNpTENKbGVIQWlPakUzTWpNeE16ZzVNRGdzSW01aVppSTZNVGN5TXpBME5qSTJNaXdpYVdGMElqb3hOekl6TURRMk1qWXlMQ0pxZEdraU9pSTBObVUzTkRNMVlpMHhNMkZoTFRSbE5tWXRPRFF6WWkwNFlqazBNbUk0TmpCak1UTWlmUS5oUkpoS3pCRTVWWlR0TTd1NEM3N2ZSaUluYjVwZHdsNWk2SEt2TmNscFdlNWlyZHpRZEUxOHc0X2NzcF9Ia0REMWFtZkRUVWs0WFhBVGVYQXNmUTdQMG1ORFgwVVV4MFp6dFljMTYtVnRMeUluQmpPZE5tdC1FUnhCdEt6WTVBTHc5OWMtWGFrVnZhUGpuVHVpUkFXZzduRjlDZEYwbmdLUUFrYkhqNjN4cDAiLCJBUEktS0VZIjoicE9ydXhMWVoiLCJpYXQiOjE3MjMwNDYzMjIsImV4cCI6MTcyMzEzODkwOH0.njs9YJ0V4sRHBt5K6T97LmYa3AF76hzEYUTmqpo5lOH5R6zNDU2oGAxz9kTITX6-iphCcmIO3RZBgofHhWpTIQ"
    # jwt_token="eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IkE1ODAzMzQ5NyIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKU1V6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUoxYzJWeVgzUjVjR1VpT2lKamJHbGxiblFpTENKMGIydGxibDkwZVhCbElqb2lkSEpoWkdWZllXTmpaWE56WDNSdmEyVnVJaXdpWjIxZmFXUWlPakVzSW5OdmRYSmpaU0k2SWpNaUxDSmtaWFpwWTJWZmFXUWlPaUk0T1RneU5tTXhNaTFpTURoa0xUTTJNVFV0T1RNNVlpMWlNelZsTnpKaE4yVTNNR01pTENKcmFXUWlPaUowY21Ga1pWOXJaWGxmZGpFaUxDSnZiVzVsYldGdVlXZGxjbWxrSWpveExDSndjbTlrZFdOMGN5STZleUprWlcxaGRDSTZleUp6ZEdGMGRYTWlPaUpoWTNScGRtVWlmWDBzSW1semN5STZJblJ5WVdSbFgyeHZaMmx1WDNObGNuWnBZMlVpTENKemRXSWlPaUpCTlRnd016TTBPVGNpTENKbGVIQWlPakUzTWpNeE5EQXhOakFzSW01aVppSTZNVGN5TXpBME56Z3pOaXdpYVdGMElqb3hOekl6TURRM09ETTJMQ0pxZEdraU9pSXdZVEEzTm1ZeU9TMDFZekpoTFRSak5tRXRZVGhsTXkxa09EbGxOR1JrWm1GbE9EUWlmUS5ZYTFTNHZSZmNZci1SUlJoNnc0WW1SWGFnVXZod2Fhb2xyaGtKUWFoRlJWYzZPaVJDcFFXLUhET0ROQ2lZdy1FanVDRjIzNTVXTnhVMjBQeUtSLVNGZWtlRXFJZ2o4NnRtUDlMbjlQamltb0gyeDZhVXNvaFBuZnFUQTR3Nm8yeHc1Y1hycEU3TjlGT1VCdXhXazBXbXcxOFhzLVhkZXIzRUNZWWRkbm91R00iLCJBUEktS0VZIjoicE9ydXhMWVoiLCJpYXQiOjE3MjMwNDc4OTYsImV4cCI6MTcyMzE0MDE2MH0.xvHU4-X2dQYBHgR4AIwLKFdmq3HzewCvcj3u9XVACt3kgpfB3Ki7h6G5GnjchD6ZcdGJ4SYWlGTzTYgujqknVA"
    # feedToken="eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IkE1ODAzMzQ5NyIsImlhdCI6MTcyMzA0Nzg5NiwiZXhwIjoxNzIzMTM0Mjk2fQ.tBiLciAcsh8qmEWa7U4wiYeE2miDSl5AllyuyBModDp5rK0MCiSpkhqZa_wciQA8-q0m142lZLMlhvDr-nx-dQ"
    #
    # broker_api_token = "RQFCDA2ZX2DMFZ5GR6HXXPFITY"
    # smartApi = SmartConnect(broker_api_token)
    # smartApi.__init__(refresh_token=refreshToken, feed_token=feedToken, access_token=jwt_token,api_key="pOruxLYZ")
    # print(smartApi.getProfile(refreshToken))
    # print(smartApi.holding())
    # try:
    #     import http.client
    #     import mimetypes
    #     conn = http.client.HTTPSConnection(
    #         "apiconnect.angelbroking.com"
    #     )
    #     # payload = "{\n\"clientcode\":\"A58033497\",\n\"password\":\"1005\"\n,\n\"totp\":\"302310\"\n}"
    #     broker_user_id="A58033497"
    #     mpin="1005"
    #     totp="263737"
    #     payload = "{\n\"clientcode\":\""+broker_user_id+"\",\n\"password\":\""+mpin+"\"\n,\n\"totp\":\""+totp+"\"\n}"
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'Accept': 'application/json',
    #         'X-UserType': 'USER',
    #         'X-SourceID': 'WEB',
    #         'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
    #         'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
    #         'X-MACAddress': 'MAC_ADDRESS',
    #         'X-PrivateKey': 'pOruxLYZ'
    #     }
    #     conn.request(
    #         "POST",
    #         "/rest/auth/angelbroking/user/v1/loginByPassword", str(payload), headers)
    #
    #     res = conn.getresponse()
    #     data = res.read()
    #     print(data.decode("utf-8"))
    # except Exception as e:
    #     print(e)
    print(time.time())
    #AngelOneAuth("antonyrajan.d@gmail.com")
    user_token_data = UserAuthTokens.objects.filter(user_id="kamezwaran.r@gmail.com")
    if list(user_token_data.values()).__len__() > 0:
        user_token_data = list(user_token_data.values())[0]
        smartApi = SmartConnect("pOruxLYZ")
        smartApi.__init__(refresh_token=user_token_data["refreshToken"], feed_token=user_token_data["feedToken"], access_token=user_token_data["jwtToken"],api_key="fSe5lcvn")
        print(smartApi.getProfile(user_token_data["refreshToken"]))
        print(smartApi.holding())
    print(time.time())
    return JsonResponse({STATUS: SUCCESS, MESSAGE: str("result.state")})
