from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..serializers.UserSerializer import UserSerializer, UserSerializerForRegister
from ..utils.FolderUtils import FolderUtils
from ..utils.FileUtils import FileUtils
from ..utils.Authentication import create_access_token
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from django.db.models import Q
from ..models import User
from drf_yasg.utils import swagger_auto_schema, no_body, status
from drf_yasg import openapi


class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        auto_schema=None
    )
    def create(self, request):
        data = request.data
        user = FolderUtils(data).createUserFolder()
        user_serializer = self.get_serializer(data=user)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(user_serializer.data)

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
        user_id = request.query_params.get('user_id')
        file = request.data['file']
        file_path = FileUtils(file, user_id).moveProfilePhotoToUserFolder()
        user = User.objects.get(id=user_id)
        user.profile_photo_path = file_path
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)

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
        email = request.data['username']
        password = request.data['password']
        user = User.objects.get(username=email)
        if (user.check_password(password)):
            token = create_access_token(user.id)
            return Response(token)
        return Response({'error': 'Invalid email or password'})

    @swagger_auto_schema(
        request_body=UserSerializerForRegister,
        responses={status.HTTP_200_OK: UserSerializer},
    )
    @action(methods=['POST'], detail=False, url_path='register', permission_classes=[AllowAny])
    def register(self, request):
        data = request.data
        user = FolderUtils(data).createUserFolder()
        hashed_password = make_password(user['password'])
        user['password'] = hashed_password
        user_serializer = self.get_serializer(data=user)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(user_serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY,
                              description="User ID", type=openapi.TYPE_STRING, required=True)
        ],
        request_body=no_body
    )
    @action(methods=['GET'], detail=False, url_path='getanotherusers')
    def get_another_users(self, request):
        user_id = request.query_params.get('user_id')
        users = User.objects.filter(~Q(id=user_id))
        serializer = self.get_serializer(users, many=True)

        return Response(serializer.data)
