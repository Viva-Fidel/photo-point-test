from rest_framework import viewsets

from .models import Notification
from .serializers import NotificationSerializer
from .tasks import send_notification

# Create your views here.


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        notification = serializer.save()
        send_notification.delay(notification.id)
