from ..serializers.PostSerializer import PostSerializer
from ..models import Post, User
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework.decorators import action
from ..middleware.PaginationBackend import CustomPagination
from django.core.paginator import Paginator
PAGE_SIZE = 20


class PostViewset(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination

    def create(self, request):
        user_id = request.query_params.get('user_id')
        data = request.data
        data['user'] = user_id
        post_serializer = PostSerializer(data=data)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        return Response(post_serializer.data)

    @action(detail=False, methods=['GET'], url_path='getpostsbyuser')
    def get_posts_by_user(self, request: Request):
        user_id = request.query_params.get('user_id')
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(user=user)

        page = self.paginate_queryset(posts)
        data = PostSerializer(page, many=True)

        return self.get_paginated_response(data.data)
