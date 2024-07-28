import requests
import argparse
TELEGRAM_IDS = ["710817544","648567264","1161672280"]


def sendMessageInTelegram(message):
    try:
        botId = "5962420966:AAEWI5ym4lIFUuRziUc-M21NcWng4uxRjgU"
        url = "https://api.telegram.org/bot" + botId + "/sendMessage"

        for user_id in TELEGRAM_IDS:
            payload = {
                'text': message,
                'chat_id': user_id
            }

            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }

            response = requests.post(url=url, params=payload, headers=headers)
    except Exception as e:
        # addLogToFile("COMMON", "exception in sendMessageInTelegram  -----  " + str(e))
        print("Exception in SendMessage via Telegram")

parser = argparse.ArgumentParser(description="Process some parameters.")
parser.add_argument('url', type=str, help='A parameter for the script')
args = parser.parse_args()
sendMessageInTelegram(args.url)