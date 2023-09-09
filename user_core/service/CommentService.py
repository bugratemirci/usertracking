from rest_framework.response import Response
from ..models import User
from ..serializers.CommentSerializer import CommentSerializer
from ..exception.BadRequestException import BadRequestException


class CommentSercice:
    def __init__(self, request) -> None:
        self.request = request

    def create(self):
        user_id = self.request.query_params.get('user_id')
        post_id = self.request.query_params.get('post_id')

        data = self.request.data
        data['post'] = post_id

        comment_serializer = CommentSerializer(data=data)
        if (comment_serializer.is_valid()):
            user = User.objects.get(id=user_id)
            comment_serializer.validated_data['user'] = user
            comment_serializer.save()
            return comment_serializer.data
        else:
            raise BadRequestException("Error")
