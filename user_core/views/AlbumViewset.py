from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import User, Photo, Album
from ..serializers.AlbumSerializer import AlbumSerializer
from ..middleware.PaginationBackend import CustomPagination
from ..service.AlbumService import AlbumService
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi


class AlbumViewset(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    pagination_class = CustomPagination

    # TODO:If the album's photos remain empty for more than 2 days, the album will be deleted automatically.
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY,
                              description="User ID", type=openapi.TYPE_STRING, required=True),
        ],
    )
    def create(self, request):
        return Response(AlbumService(request=request).create())

    @action(detail=False, methods=['PUT'], url_path='addphototoalbum')
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('photo_id', openapi.IN_QUERY,
                              description="Photo ID", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('album_id', openapi.IN_QUERY,
                              description="Album ID", type=openapi.TYPE_STRING, required=True),

        ],
        request_body=no_body
    )
    def add_photo_to_album(self, request):
        return Response(AlbumService(request=request).addPhotoToAlbum())

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY,
                              description="User ID", type=openapi.TYPE_STRING, required=True),
        ],
        paginator_inspectors=None
    )
    @action(detail=False, methods=['GET'], url_path='getalbumsbyuser')
    def get_albums_by_user(self, request):
        return Response(AlbumService(request=request).getAlbumsByUser())
