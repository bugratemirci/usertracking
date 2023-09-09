from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema, no_body, status
from drf_yasg import openapi

from ..service.UserService import UserService
from ..serializers.UserSerializer import UserSerializer, UserSerializerForRegister
from ..middleware.PaginationBackend import CustomPagination
from ..models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['username', 'email']
    search_fields = ['username', 'email']

    @swagger_auto_schema(
        auto_schema=None
    )
    def create(self, request):
        return Response(UserService(request=request).create())

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY,
                              description="User ID", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('file', openapi.IN_QUERY,
                              description="Photo", type=openapi.TYPE_FILE, required=True)
        ],
        request_body=no_body
    )
    @action(methods=['PUT'], detail=False, url_path='uploadprofilephoto')
    def upload_profile_photo(self, request):
        return Response(UserService(request=request).uploadPhoto())

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_QUERY,
                              description="Username", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('password', openapi.IN_QUERY,
                              description="Password", type=openapi.TYPE_STRING, required=True)
        ],
        request_body=no_body
    )
    @action(methods=['POST'], detail=False, url_path='login', permission_classes=[AllowAny])
    def login(self, request):
        return Response(UserService(request=request).login())

    @swagger_auto_schema(
        request_body=UserSerializerForRegister,
        responses={status.HTTP_200_OK: UserSerializer},
    )
    @action(methods=['POST'], detail=False, url_path='register', permission_classes=[AllowAny])
    def register(self, request,):
        return Response(UserService(request=request).register())

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY,
                              description="User ID", type=openapi.TYPE_STRING, required=True)
        ],
        request_body=no_body
    )
    @action(methods=['GET'], detail=False, url_path='getanotherusers')
    def get_another_users(self, request):
        return Response(UserService(request=request).getAnotherUser())
