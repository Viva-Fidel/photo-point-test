

from .utils import EmailChannel, SmsChannel, TelegramChannel


from .channels.email import EmailChannel
from .channels.sms import SmsChannel
from .channels.telegram import TelegramChannel


class NotificationManager:
    def __init__(self, channel_configs=None):

        configs = channel_configs or {}
        self.channels = [
            EmailChannel(**configs.get("email", {})),
            SmsChannel(**configs.get("sms", {})),
            TelegramChannel(**configs.get("telegram", {})),
        ]

        # Сортируем по приоритету
        self.channels = sorted(self.channels, key=lambda ch: ch.priority)

    def send(self, notification):
        errors = []

        for channel in self.channels:
            if not channel.enabled:
                continue

            try:
                channel.send(notification.user, notification.message)
                notification.status = notification.Status.SENT
                notification.sent_channel = channel.name
                notification.is_sent = True
                notification.save()
                return
            except Exception as e:
                errors.append(f"{channel.name}: {str(e)}")

        notification.status = notification.Status.FAILED
        notification.error_log = "\n".join(errors)
        notification.save()
