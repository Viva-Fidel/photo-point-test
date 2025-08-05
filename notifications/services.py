import requests
from django.conf import settings
from django.core.mail import send_mail
from smsaero import SmsAero, SmsAeroException


def send_email(user, message):
    send_mail("Оповещение", message, settings.EMAIL_HOST_USER, [user.email])


def send_sms(user, message):
    if not user.phone:
        raise ValueError("У пользователя нет номера телефона")

    try:
        api = SmsAero(settings.SMSAERO_EMAIL, settings.SMSAERO_API_KEY)

        response = api.send_sms(user.phone, message)

        if not response.get("success"):
            raise Exception(f"Ошибка SMSAero: {response}")
        return response
    except SmsAeroException as e:
        raise Exception(f"Ошибка SMSAero: {str(e)}")


def send_telegram(user, message):
    if not user.telegram_username:
        raise ValueError("У пользователя нет аккаунта в Telegram")

    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = f"@{user.telegram_username}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Ошибка Telegram: {str(e)}")
