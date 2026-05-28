import requests


def get_bot_config():
    from plutusAI.models import TelegramBotConfig

    config = TelegramBotConfig.objects.first()
    if config:
        return {
            "bot_id": config.bot_id,
            "admin_bot_id": config.admin_bot_id,
            "admin_chat_ids": config.admin_chat_ids,
        }
    return {"bot_id": None, "admin_bot_id": None, "admin_chat_ids": ""}


def sendMessageInTelegram(message, user_email=None):
    try:
        config = get_bot_config()

        if user_email:
            from plutusAI.models import TelegramSettings

            settings = TelegramSettings.objects.filter(user_id=user_email).first()
            if settings and settings.notify_on_error and settings.chat_id:
                bot_id = config["bot_id"]
                if not bot_id:
                    return
                url = f"https://api.telegram.org/bot{bot_id}/sendMessage"
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
                for chat_id in settings.chat_id.split(","):
                    chat_id = chat_id.strip()
                    if chat_id:
                        payload = {"text": message, "chat_id": chat_id}
                        requests.post(url=url, params=payload, headers=headers)
                return

        admin_bot_id = config["admin_bot_id"] or config["bot_id"]
        admin_ids = [
            c.strip() for c in config["admin_chat_ids"].split(",") if c.strip()
        ]
        if not admin_bot_id or not admin_ids:
            return
        url = f"https://api.telegram.org/bot{admin_bot_id}/sendMessage"
        for chat_id in admin_ids:
            payload = {"text": message, "chat_id": chat_id}
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            requests.post(url=url, params=payload, headers=headers)
    except Exception:
        print("Exception in SendMessage via Telegram")
