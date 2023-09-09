from rest_framework import serializers
from ..models import Comment, User
from .UserSerializerForComment import UserSerializerForComment


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
