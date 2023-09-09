from ..serializers.PostSerializer import PostSerializer, PostSerializerWithUser
from ..models import Post, User
from ..exception.BadRequestException import BadRequestException


class PostService:
    def __init__(self, request) -> None:
        self.request = request

    def create(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id == None:
            raise BadRequestException("User ID can't null.")
        data = self.request.data
        data['user'] = user_id
        post_serializer = PostSerializer(data=data)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        return post_serializer.data

    def getAll(self, paginate_queryset, get_paginated_response):
        posts = Post.objects.all()

        page = paginate_queryset(posts)
        data = PostSerializerWithUser(page, many=True)

        return get_paginated_response(data.data)

    def getAllByUser(self, paginate_queryset, get_paginated_response):
        user_id = self.request.query_params.get('user_id')
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(user=user)

        page = paginate_queryset(posts)
        data = PostSerializerWithUser(page, many=True)

        return get_paginated_response(data.data)

    def getPostsWithComments(self, paginate_queryset, get_paginated_response):
        posts = Post.objects.all()
        page = paginate_queryset(posts)
        data = PostSerializerWithUser(page, many=True)

        return get_paginated_response(data.data)
