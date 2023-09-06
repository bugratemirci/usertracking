from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..models import User, Photo, Album
from ..serializers.AlbumSerializer import AlbumSerializer

from rest_framework.decorators import action


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

    @action(detail=False, methods=['GET'], url_path='getalbumsbyuser')
    def get_albums_by_user(self, request):
        user_id = request.query_params.get('user_id')
        user = User.objects.get(id=user_id)
        albums = Album.objects.filter(user=user)
        data = AlbumSerializer(albums, many=True)

        return Response(data.data)
