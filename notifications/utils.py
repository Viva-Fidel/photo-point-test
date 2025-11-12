import requests
from django.conf import settings
from django.core.mail import send_mail
from smsaero import SmsAero, SmsAeroException

from abc import ABC, abstractmethod


class BaseChannel(ABC):

    def __init__(self, enabled = True, priority = 10):
        self.enabled = enabled
        self.priority = priority 

    @abstractmethod
    def send(self, user, message: str):
        pass

class EmailChannel(BaseChannel):

    def send(self, user, message):
        if not user.email:
            raise ValueError("У пользователя нет email")
        send_mail(
            subject="Оповещение",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )


class SmsChannel(BaseChannel):

    def send(self, user, message: str):
        if not user.phone:
            raise ValueError("У пользователя нет номера телефона")

        api = SmsAero(settings.SMSAERO_EMAIL, settings.SMSAERO_API_KEY)
        response = api.send_sms(user.phone, message)

        if not response.get("success"):
            raise Exception(f"Ошибка SMSAero: {response}")
        
class TelegramChannel(BaseChannel):

    def send(self, user, message: str):
        if not user.telegram_username:
            raise ValueError("У пользователя нет Telegram аккаунта")

        token = settings.TELEGRAM_BOT_TOKEN
        chat_id = f"@{user.telegram_username}"
        url = f"https://api.telegram.org/bot{token}/sendMessage"

        response = requests.post(url, json={"chat_id": chat_id, "text": message}, timeout=10)
        response.raise_for_status()