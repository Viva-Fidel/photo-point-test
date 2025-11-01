

from .utils import EmailChannel, SmsChannel, TelegramChannel


class NotificationService:
    def __init__(self):
        self.channels = [EmailChannel(), TelegramChannel(), SmsChannel()]

    def send(self, notification):
        errors = []

        for channel in self.channels:
            try:
                channel.send(notification.user, notification.message)
                notification.status = notification.Status.SENT
                notification.sent_channel = channel.__class__.__name__
                notification.is_sent = True
                notification.save()
                return
            except Exception as e:
                errors.append(f"{channel.__class__.__name__}: {str(e)}")

        notification.status = notification.Status.FAILED
        notification.error_log = "\n".join(errors)
        notification.save()