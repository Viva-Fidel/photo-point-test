from rest_framework import viewsets

from .models import CustomUser
from .serializers import UserSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
