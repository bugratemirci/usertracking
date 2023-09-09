from rest_framework import serializers
from ..models import User


class UserSerializerForRegister(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'username', 'email',
                  'phone', 'password', 'root_path', 'id')
