from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..models import User, Photo, Album
from ..serializers.PhotoSerializer import PhotoSerializer
from ..middleware.PaginationBackend import CustomPagination

from ..utils.FileUtils import FileUtils
from rest_framework.decorators import action


class PhotoViewset(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    pagination_class = CustomPagination

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

    @action(methods=['GET'], detail=False, url_path='getphotosbyuser')
    def get_photos_by_user(self, request):
        user_id = request.query_params.get('user_id')
        user = User.objects.get(id=user_id)
        photos = Photo.objects.filter(user=user)
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='getphotosbyalbum')
    def get_photos_by_album(self, request):
        album_id = request.query_params.get('album_id')
        album = Album.objects.get(id=album_id)
        photos = Photo.objects.filter(album=album)
        photo_serializer = PhotoSerializer(photos, many=True)
        return Response(photo_serializer.data)
