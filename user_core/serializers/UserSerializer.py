from rest_framework import serializers
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'email', 'phone', 'website', 'company', 'address',
                  'root_path', 'profile_photo_path')


class UserSerializerForRegister(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'phone', 'password')


class UserSerializerForComment(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'profile_photo_path']
