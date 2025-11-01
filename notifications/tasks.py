from photo_point.celery import app

from .models import Notification
from .services import NotificationService


@app.task(bind=True, max_retries=3)
def send_notification(self, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        return

    service = NotificationService() 
    service.send(notification)
