from photo_point.celery import app

from .models import Notification
from .services import send_email, send_sms, send_telegram


@app.task(bind=True, max_retries=3)
def send_notification(self, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        return

    errors = []

    # Сначала почта, потом тelegram, потом SMS
    channels = [
        Notification.Channel.EMAIL,
        Notification.Channel.TELEGRAM,
        Notification.Channel.SMS,
    ]

    for channel in channels:
        try:
            if channel == Notification.Channel.EMAIL:
                send_email(notification.user, notification.message)
            elif channel == Notification.Channel.TELEGRAM:
                send_telegram(notification.user, notification.message)
            elif channel == Notification.Channel.SMS:
                send_sms(notification.user, notification.message)

            notification.status = Notification.Status.SENT
            notification.sent_channel = channel
            notification.is_sent = True
            notification.save()
            return
        except Exception as e:
            errors.append(f"{channel}: {str(e)}")

    # Если попытки провалились, сохраняем ошибки
    notification.status = Notification.Status.FAILED
    notification.error_log = "\n".join(errors)
    notification.save()
