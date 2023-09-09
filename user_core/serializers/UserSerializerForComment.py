from rest_framework import serializers
from ..models import User


class UserSerializerForComment(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'profile_photo_path']
