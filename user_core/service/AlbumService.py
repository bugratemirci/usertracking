from ..models import User, Photo, Album
from ..serializers.AlbumSerializer import AlbumSerializer
from ..exception.BadRequestException import BadRequestException


class AlbumService:
    def __init__(self, request) -> None:
        self.request = request

    def create(self):
        user_id = self.request.query_params.get('user_id')
        if user_id == None:
            raise BadRequestException("User id cant't be null.")
        data = self.request.data
        data['user'] = user_id
        album_serializer = AlbumSerializer(data=data)
        album_serializer.is_valid(raise_exception=True)
        album_serializer.save()
        return album_serializer.data

    def addPhotoToAlbum(self):
        photo_id = self.request.query_params.get('photo_id', None)
        album_id = self.request.query_params.get('album_id', None)
        if album_id == None or photo_id == None:
            raise BadRequestException("Album id or Photo id cant't be null.")

        photo = Photo.objects.get(id=photo_id)
        album = Album.objects.get(id=album_id)
        album.photos.add(photo)
        album.save()
        serializer = AlbumSerializer(album)

        return serializer.data

    def getAlbumsByUser(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id == None:
            raise BadRequestException("User id cant't be null.")
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise BadRequestException("User not found!")
        albums = Album.objects.filter(user=user)
        serializer = AlbumSerializer(albums, many=True)

        return serializer.data
