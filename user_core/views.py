from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import User, Post, Comment, Todo
from .serializers import UserSerializer, PostSerializer, CommentSerializer, TodoSerializer


class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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


class CommentViewset(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

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


class TodoViewset(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def create(self, request):
        user_id = request.query_params.get('user_id')
        data = request.data

        data['user'] = user_id

        todo_serializer = self.get_serializer(data=data)
        todo_serializer.is_valid(raise_exception=True)
        todo_serializer.save()
        return Response(todo_serializer.data)
