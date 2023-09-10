from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..models import Photo
from ..serializers.PhotoSerializer import PhotoSerializer
from ..middleware.PaginationBackend import CustomPagination

from ..service.PhotoService import PhotoService
from rest_framework.decorators import action


class PhotoViewset(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    pagination_class = CustomPagination

    def create(self, request):
        return Response(PhotoService(request=request).create())

    @action(methods=['GET'], detail=False, url_path='getphotosbyuser')
    def get_photos_by_user(self, request):
        return Response(PhotoService(request=request).getPhotoByUser())

    @action(methods=['GET'], detail=False, url_path='getphotosbyalbum')
    def get_photos_by_album(self, request):
        return Response(PhotoService(request=request).getPhotosByAlbum())

    @action(methods=['DELETE'], detail=False, url_path='deletephoto')
    def delete_photo(self, request):
        return Response(PhotoService(request=request).deletePhoto())
