from datetime import datetime

from SmartApi import SmartConnect
from celery.result import AsyncResult
import time
from django.http import JsonResponse
from plutusAI.models import BrokerDetails
from plutusAI.server.base import addLogDetails, getTokenUsingSymbol, getTradingSymbol, current_time
from plutusAI.server.broker.AngelOneBroker import AngelOneBroker
from plutusAI.server.constants import *


def testerCheck(request):
    refreshToken = "eyJhbGciOiJIUzUxMiJ9.eyJ0b2tlbiI6IlJFRlJFU0gtVE9LRU4iLCJSRUZSRVNILVRPS0VOIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5WDNSNWNHVWlPaUpqYkdsbGJuUWlMQ0owYjJ0bGJsOTBlWEJsSWpvaWRISmhaR1ZmY21WbWNtVnphRjkwYjJ0bGJpSXNJbWR0WDJsa0lqb3dMQ0prWlhacFkyVmZhV1FpT2lJNE9UZ3lObU14TWkxaU1EaGtMVE0yTVRVdE9UTTVZaTFpTXpWbE56SmhOMlUzTUdNaUxDSnJhV1FpT2lKMGNtRmtaVjlyWlhsZmRqRWlMQ0p2Ylc1bGJXRnVZV2RsY21sa0lqb3dMQ0pwYzNNaU9pSnNiMmRwYmw5elpYSjJhV05sSWl3aWMzVmlJam9pUVRVNE1ETXpORGszSWl3aVpYaHdJam94TnpJeU1UWTNPREl4TENKdVltWWlPakUzTWpFNU9UUTVOakVzSW1saGRDSTZNVGN5TVRrNU5EazJNU3dpYW5ScElqb2lNREJsTlRJNVptRXROVEppTVMwMFlqVXhMV0UwTTJZdE1tRTBNR1l4TjJSbFlUWTNJbjAuaWl5czNMY1VVd3ZveGVzVmRZVXVPcDFYVVo3ZU4wLTRpelk4aXRKOG94SmNKNHNDZjFpdzZrUWVSaDdKTU5OQUNzb3RvWVdMYVVXdV9SU29jcm53WGRWMW9NOUJRbHZ4N1hvTlJBQjZVOVlubzJoY0NSYW45TFlfVXM2RDlqQ2JpNmpTTHpja3FtUHFxd2V4YlJ4Q3gxOTJFSFpWZlhOSWxreUduS0lGOS1VIiwiaWF0IjoxNzIxOTk1MDIxfQ.uf47t2xfbo2c2W0ld7e3c5dWTKvCVqXmc8u0vAW4g13JNhkdOjzmnBdADvfHPuaYqLfGV1EAxke-L09phK7M0Q"
    auth_token = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IkE1ODAzMzQ5NyIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKU1V6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUoxYzJWeVgzUjVjR1VpT2lKamJHbGxiblFpTENKMGIydGxibDkwZVhCbElqb2lkSEpoWkdWZllXTmpaWE56WDNSdmEyVnVJaXdpWjIxZmFXUWlPakVzSW5OdmRYSmpaU0k2SWpNaUxDSmtaWFpwWTJWZmFXUWlPaUk0T1RneU5tTXhNaTFpTURoa0xUTTJNVFV0T1RNNVlpMWlNelZsTnpKaE4yVTNNR01pTENKcmFXUWlPaUowY21Ga1pWOXJaWGxmZGpFaUxDSnZiVzVsYldGdVlXZGxjbWxrSWpveExDSndjbTlrZFdOMGN5STZleUprWlcxaGRDSTZleUp6ZEdGMGRYTWlPaUpoWTNScGRtVWlmWDBzSW1semN5STZJblJ5WVdSbFgyeHZaMmx1WDNObGNuWnBZMlVpTENKemRXSWlPaUpCTlRnd016TTBPVGNpTENKbGVIQWlPakUzTWpJd09EUXdNVElzSW01aVppSTZNVGN5TVRrNU1qTXpOQ3dpYVdGMElqb3hOekl4T1RreU16TTBMQ0pxZEdraU9pSmlZMkU1WkRJeE1pMHhPREkwTFRSalltTXRZV00wWVMxbVlUSTNORGc1T0dNME9XTWlmUS5SQVhjV0xoYTFpN1MtQV9Qc3MyaTg4czVGRUZNbURKUFU5Vkl6ZzVJVE0wcmFueTZ0OUFyajZiS1k5czJjUnZLMFlTYXl3VWM3VzdQTGxRZG5iWkQzSVZ1U052cHFOLXY5aGdLLWlUVkdoQzR0WXJFYkwwcC1welhqaWJmMVdrTXZzb2NGSnc0SkFERmtiS2pRWVF5SVViMTVjY0g2Ymw3ZjRCZXNjYVprOHciLCJBUEktS0VZIjoicE9ydXhMWVoiLCJpYXQiOjE3MjE5OTIzOTQsImV4cCI6MTcyMjA4NDAxMn0.2BGuVXNTKXQ01h6dwlGMX2jR1ry7YwE8Eeb_ujYwQaynMdUnANQimOHuXjRKeU-eAPlvhhjHIuOEatL8BqSlxg"
    jwt_token="eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IkE1ODAzMzQ5NyIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKU1V6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUoxYzJWeVgzUjVjR1VpT2lKamJHbGxiblFpTENKMGIydGxibDkwZVhCbElqb2lkSEpoWkdWZllXTmpaWE56WDNSdmEyVnVJaXdpWjIxZmFXUWlPakVzSW5OdmRYSmpaU0k2SWpNaUxDSmtaWFpwWTJWZmFXUWlPaUk0T1RneU5tTXhNaTFpTURoa0xUTTJNVFV0T1RNNVlpMWlNelZsTnpKaE4yVTNNR01pTENKcmFXUWlPaUowY21Ga1pWOXJaWGxmZGpFaUxDSnZiVzVsYldGdVlXZGxjbWxrSWpveExDSndjbTlrZFdOMGN5STZleUprWlcxaGRDSTZleUp6ZEdGMGRYTWlPaUpoWTNScGRtVWlmWDBzSW1semN5STZJblJ5WVdSbFgyeHZaMmx1WDNObGNuWnBZMlVpTENKemRXSWlPaUpCTlRnd016TTBPVGNpTENKbGVIQWlPakUzTWpJd09EVTFPREVzSW01aVppSTZNVGN5TVRrNU5EazJNU3dpYVdGMElqb3hOekl4T1RrME9UWXhMQ0pxZEdraU9pSmtaV0ZtTVRZd05TMHdZemhtTFRRd1pEWXRPVEl6TkMwNU9EYzFNV0k1WldVeU9EQWlmUS5XOHJ0WFpWaEpLQ3ZPWDRTUUxEbi1aQ2lfWXB4TnMxSE8wS3RGbEw5ZnNHR3hPcUhsbmhLd0RpWEZmS3dmdDloRFdveEg0cHNCczRVUmgyZi14ZmltT3pxcUExOG1VanRhbHViMU4wcG1UMF9aMlI0MkZrVnQzd0dUdzdCdjBBM2lzbTEwY21RLU91X0ZLSWhPMGNsVVlQWXBYMEdDQUxLVGZQX2RrZXhmTFUiLCJBUEktS0VZIjoicE9ydXhMWVoiLCJpYXQiOjE3MjE5OTUwMjEsImV4cCI6MTcyMjA4NTU4MX0.lUUvlWFzTgy-6V6hDMhu0nBh4GuKpVsSK_s5tqFf3EqOYCIM-z-hAldixBtjvmrBeKsWGXonP5vQH899BXICiw"
    feedToken="eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IkE1ODAzMzQ5NyIsImlhdCI6MTcyMTk5NTAyMSwiZXhwIjoxNzIyMDgxNDIxfQ.R8lf1KSJJwjtWVKkCt9D6tkj2UT_yqUgjrSnTFYGPLlaStn4Y79biCtZ2OQJIUFX3HoH5FoHpBuk3jZV6p3vPg"

    broker_api_token = "RQFCDA2ZX2DMFZ5GR6HXXPFITY"
    smartApi = SmartConnect(broker_api_token)
    smartApi.__init__(refresh_token=refreshToken, feed_token=feedToken, access_token=jwt_token,api_key="pOruxLYZ")
    print(smartApi.getProfile(refreshToken))
    # try:
    #     import http.client
    #     import mimetypes
    #     conn = http.client.HTTPSConnection(
    #         "apiconnect.angelbroking.com"
    #     )
    #     payload = "{\n\"clientcode\":\"A58033497\",\n\"password\":\"1005\"\n,\n\"totp\":\"024367\"\n}"
    #
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
    #         "/rest/auth/angelbroking/user/v1/loginByPassword", payload, headers)
    #
    #     res = conn.getresponse()
    #     data = res.read()
    #     print(data.decode("utf-8"))
    # except Exception as e:
    #     print(e)
    return JsonResponse({STATUS: SUCCESS, MESSAGE: str("result.state")})
