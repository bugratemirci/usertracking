from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import User, Post, Comment, Todo, Photo, Album
from .serializers import UserSerializer, PostSerializer, CommentSerializer, TodoSerializer, PhotoSerializer, AlbumSerializer
from .utils.FolderUtils import FolderUtils
from .utils.FileUtils import FileUtils
from rest_framework.decorators import action


class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        data = request.data
        user = FolderUtils(data).createUserFolder()
        user_serializer = self.get_serializer(data=user)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(user_serializer.data)

    @action(methods=['PUT'], detail=False, url_path='uploadprofilephoto')
    def upload_profile_photo(self, request):
        user_id = request.query_params.get('user_id')
        file = request.data['file']
        file_path = FileUtils(file, user_id).moveProfilePhotoToUserFolder()
        user = User.objects.get(id=user_id)
        user.profile_photo_path = file_path
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


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


class PhotoViewset(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def create(self, request):
        user_id = request.query_params.get('user_id')
        title = request.data['title']
        file = request.data['file']
        file_path = FileUtils(file, user_id).movePhotoFileToUserFolder()
        data = request.data

        data['user'] = user_id
        data['title'] = title
        data['url'] = file_path
        data['thumbnail_url'] = file_path
        photo_serializer = self.get_serializer(data=data)
        photo_serializer.is_valid(raise_exception=True)
        photo_serializer.save()
        return Response(photo_serializer.data)


class AlbumViewset(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    # TODO:If the album's photos remain empty for more than 2 days, the album will be deleted automatically.

    def create(self, request):
        user_id = request.query_params.get('user_id')
        data = request.data
        data['user'] = user_id
        album_serializer = self.get_serializer(data=data)
        album_serializer.is_valid(raise_exception=True)
        album_serializer.save()
        return Response(album_serializer.data)

    @action(detail=False, methods=['PUT'], url_path='addphototoalbum')
    def add_photo_to_album(self, request):
        photo_id = request.query_params.get('photo_id')
        album_id = request.query_params.get('album_id')
        photo = Photo.objects.get(id=photo_id)
        album = Album.objects.get(id=album_id)
        album.photos.add(photo)
        album.save()
        serializer = AlbumSerializer(album)
        return Response(serializer.data)
