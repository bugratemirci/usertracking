from ..serializers.PostSerializer import PostSerializer
from ..models import Post
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from rest_framework.decorators import action
from ..middleware.PaginationBackend import CustomPagination
from ..service.PostService import PostService


class PostViewset(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination

    def create(self, request):
        return Response(PostService(request).create())

    def list(self, request, *args, **kwargs):
        return PostService(None).getAll(self.paginate_queryset, self.get_paginated_response)

    @action(detail=False, methods=['GET'], url_path='getpostswithcomments')
    def get_posts_with_comments(self, request):
        return PostService(request=request).getPostsWithComments(self.paginate_queryset, self.get_paginated_response)

    @action(detail=False, methods=['GET'], url_path='getpostsbyuser')
    def get_posts_by_user(self, request):
        return PostService(request=request).getAllByUser(self.paginate_queryset, self.get_paginated_response)
