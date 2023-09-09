from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..models import User, Comment
from ..serializers.CommentSerializer import CommentSerializer
from ..middleware.PaginationBackend import CustomPagination
from ..service.CommentService import CommentSercice


class CommentViewset(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    def create(self, request):
        return Response(CommentSercice(request=request).create())
