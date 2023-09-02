from rest_framework import serializers
from .models import User, Post, Comment, Todo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSerializerForComment(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'photo_path']


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_user(self, obj):
        try:
            user = User.objects.get(id=obj.user.id)
            serializer = UserSerializerForComment(user)
            return serializer.data
        except User.DoesNotExist:
            return None


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
