from django.urls import include, path
from rest_framework import routers

from .views import NotificationViewSet

app_name = "notifications"


router = routers.SimpleRouter()
router.register(
    "notification",
    NotificationViewSet,
    basename="notification",
)

urlpatterns = [
    path("api/", include(router.urls)),
]
