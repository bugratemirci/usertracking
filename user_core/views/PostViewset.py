from ..serializers.PostSerializer import PostSerializer
from ..models import Post
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


class PostViewset(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request):
        user_id = request.query_params.get('user_id')
        data = request.data
        data['user'] = user_id
        post_serializer = PostSerializer(data=data)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        return Response(post_serializer.data)
