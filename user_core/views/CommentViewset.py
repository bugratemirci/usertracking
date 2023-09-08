from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..models import User, Comment
from ..serializers.CommentSerializer import CommentSerializer
from ..middleware.PaginationBackend import CustomPagination


class CommentViewset(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    def create(self, request):
        user_id = request.query_params.get('user_id')
        post_id = request.query_params.get('post_id')

        data = request.data
        data['post'] = post_id

        comment_serializer = CommentSerializer(data=data)
        if (comment_serializer.is_valid()):
            user = User.objects.get(id=user_id)
            comment_serializer.validated_data['user'] = user
            comment_serializer.save()
            return Response(comment_serializer.data)

        return Response(comment_serializer.errors)
