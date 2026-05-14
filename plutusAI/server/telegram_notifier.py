import requests

TELEGRAM_IDS = ["710817544", "648567264"] # "1161672280"
BOT_ID = "5962420966:AAEWI5ym4lIFUuRziUc-M21NcWng4uxRjgU"


def sendMessageInTelegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_ID}/sendMessage"
        for user_id in TELEGRAM_IDS:
            payload = {"text": message, "chat_id": user_id}
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            requests.post(url=url, params=payload, headers=headers)
    except Exception:
        print("Exception in SendMessage via Telegram")
