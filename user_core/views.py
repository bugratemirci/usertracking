from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
# Create your views here.


class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
