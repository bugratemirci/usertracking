from ..serializers.PhotoSerializer import PhotoSerializer
from ..models import Photo, User, Album
from ..exception.BadRequestException import BadRequestException
from ..utils.FileUtils import FileUtils


class PhotoService:
    def __init__(self, request):
        self.request = request

    def create(self):
        user_id = self.request.query_params.get('user_id', None)
        title = self.request.data.get('title', None)
        file = self.request.data.get('file', None)

        if (user_id == None or title == None or file == None):
            raise BadRequestException(
                "Please check the data you sent! Required fields: User ID, Title, File")
        file_path = FileUtils(file, user_id).movePhotoFileToUserFolder()

        data = {
            "user": user_id,
            "title": title,
            "url": file_path,
            "thumbnail_url": file_path}

        photo_serializer = PhotoSerializer(data=data)
        photo_serializer.is_valid(raise_exception=True)
        photo_serializer.save()

        return photo_serializer.data

    def getPhotoByUser(self):
        user_id = self.request.query_params.get('user_id')
        if (user_id == None):
            raise BadRequestException(
                "Please check the data you sent! Required fields: User ID")
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise BadRequestException("User does not exists.")

        photos = Photo.objects.filter(user=user)
        serializer = PhotoSerializer(photos, many=True)
        return serializer.data

    def getPhotosByAlbum(self):
        album_id = self.request.query_params.get('album_id', None)
        if (album_id == None):
            raise BadRequestException(
                "Please check the data you sent! Required fields: Album ID")
        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            raise BadRequestException("Album does not exists.")

        photos = Photo.objects.filter(album=album)
        photo_serializer = PhotoSerializer(photos, many=True)

        return photo_serializer.data
