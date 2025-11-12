from django.conf import settings
from photo_point.celery import app
from .models import Notification
from .services import NotificationManager


@app.task(bind=True, max_retries=3)
def send_notification(self, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        return

    manager = NotificationManager(channel_configs=settings.NOTIFY_CHANNELS)
    manager.send(notification)