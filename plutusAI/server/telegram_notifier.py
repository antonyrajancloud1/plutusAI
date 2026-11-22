from datetime import datetime

import requests

TELEGRAM_MAX_LEN = 4000

# (patterns, issue, fix) — first match wins, so keep specific patterns above
# generic ones. Patterns are matched case-insensitively against the raw error.
ERROR_EXPLANATIONS = [
    (
        ["AG8004", "API key"],
        "AngelOne API key is invalid or expired.",
        "Regenerate the API key at smartapi.angelbroking.com and update it in Broker settings.",
    ),
    (
        ["AB1007", "AG8001", "Not enough segments", "Invalid Token", "token is invalid"],
        "AngelOne login session is invalid or expired.",
        "Re-login the broker from the Broker page.",
    ),
    (
        ["Request Rejected"],
        "AngelOne firewall rejected the request (too many requests or IP blocked).",
        "Usually clears in a minute. If it repeats, contact AngelOne with the support ID from the log.",
    ),
    (
        ["Read timed out", "ConnectTimeout", "Max retries exceeded", "timed out", "Connection aborted", "ConnectionError"],
        "AngelOne API did not respond (network timeout).",
        "Temporary AngelOne/network issue. Verify the order in the AngelOne app.",
    ),
    (
        ["Unable to fetch order status"],
        "Could not read the entry order status from AngelOne even after retries.",
        "Verify the entry order in the AngelOne app.",
    ),
    (
        ["Couldn't parse the JSON", "b'not found'", "b''"],
        "AngelOne returned an empty/invalid response.",
        "Temporary AngelOne issue. Verify the order in the AngelOne app.",
    ),
    (
        ["Invalid symboltoken", "AB4033"],
        "Option symbol not found in scrip master (invalid symbol token).",
        "Refresh scrip_master.json and check the expiry settings.",
    ),
    (
        ["insufficient", "margin", "RMS"],
        "AngelOne rejected the order: insufficient funds / margin (RMS).",
        "Add funds or reduce lots.",
    ),
    (
        ["Broker rejected order"],
        "AngelOne rejected the order.",
        "Check the rejection reason below and the order book in AngelOne.",
    ),
    (
        ["atm=None"],
        "Could not fetch the index spot price from AngelOne, so the strike could not be calculated.",
        "AngelOne LTP API failed. Place the entry manually if needed.",
    ),
    (
        ["Internet connection issue"],
        "Could not fetch the option LTP from AngelOne.",
        "Check AngelOne API/session status.",
    ),
    (
        ["No webhook data", "Webhook details not found"],
        "Entry order details are missing in the database for this strategy.",
        "Check the position in AngelOne and exit manually if open.",
    ),
    (
        ["Index data not found"],
        "Index configuration is missing.",
        "Add the index in Index settings.",
    ),
    (
        ["'NoneType' object"],
        "Broker returned no data (empty response).",
        "Verify the order in the AngelOne app.",
    ),
]


def explainError(error_msg):
    text = str(error_msg).lower()
    for patterns, issue, fix in ERROR_EXPLANATIONS:
        if any(p.lower() in text for p in patterns):
            return issue, fix
    return str(error_msg), None


def sendTradeAlert(title, user_email, error_msg, details=None, action=None):
    """Formats an actionable alert: what failed, for whom, why, and what to do."""
    issue, fix = explainError(error_msg)
    lines = [f"🚨 {title}", ""]
    lines.append(f"👤 User: {user_email}")
    for label, value in (details or {}).items():
        if value not in (None, ""):
            lines.append(f"• {label}: {value}")
    lines.append(f"🕒 Time: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}")
    lines.append("")
    lines.append(f"❗ Issue: {issue}")
    if action:
        lines.append(f"👉 Do now: {action}")
    if fix:
        lines.append(f"🔧 Fix: {fix}")
    lines.append("")
    lines.append(f"Raw error: {str(error_msg)[:600]}")
    sendMessageInTelegram("\n".join(lines), user_email=user_email)


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


def _post(bot_id, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_id}/sendMessage"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    payload = {"text": message[:TELEGRAM_MAX_LEN], "chat_id": chat_id}
    requests.post(url=url, json=payload, headers=headers, timeout=10)


def sendMessageInTelegram(message, user_email=None):
    # Sent to the user's own chat (if enabled) and always to the admin chats,
    # so the admin sees every user's failure.
    try:
        config = get_bot_config()
        sent_to = set()

        if user_email:
            from plutusAI.models import TelegramSettings

            settings = TelegramSettings.objects.filter(user_id=user_email).first()
            if settings and settings.notify_on_error and settings.chat_id and config["bot_id"]:
                for chat_id in settings.chat_id.split(","):
                    chat_id = chat_id.strip()
                    if chat_id:
                        _post(config["bot_id"], chat_id, message)
                        sent_to.add(chat_id)

        admin_bot_id = config["admin_bot_id"] or config["bot_id"]
        admin_ids = [
            c.strip() for c in (config["admin_chat_ids"] or "").split(",") if c.strip()
        ]
        if not admin_bot_id:
            return
        for chat_id in admin_ids:
            if chat_id not in sent_to:
                _post(admin_bot_id, chat_id, message)
    except Exception as e:
        print(f"Exception in SendMessage via Telegram: {e}")
