from rest_framework import serializers
from ..models import Post, User
from ..serializers.UserSerializer import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostSerializerWithUser(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_user(self, obj):
        try:
            user = User.objects.get(id=obj.user.id)
            serializer = UserSerializer(user)
            return serializer.data
        except User.DoesNotExist:
            return None
