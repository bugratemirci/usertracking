from rest_framework import serializers
from ..models import Post, User, Comment
from ..serializers.UserSerializer import UserSerializer
from ..serializers.CommentSerializer import CommentSerializer


class PostSerializerWithUser(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

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

    def get_comments(self, obj):
        try:
            comment = Comment.objects.filter(post=obj)
            serializer = CommentSerializer(comment, many=True)
            return serializer.data
        except:
            return None
