from django.contrib.auth.hashers import make_password
from django.db.models import Q

from ..models import User
from ..serializers.UserSerializer import UserSerializer, UserSerializerForRegister
from ..exception.BadRequestException import BadRequestException
from ..utils.Authentication import create_access_token
from ..utils.FolderUtils import FolderUtils
from ..utils.FileUtils import FileUtils
from ..utils.Authentication import decode_access_token
from ..constants.Response import UserTokenResponse


class UserService:
    def __init__(self, request):
        self.request = request

    def create(self):
        data = self.request.data
        user = FolderUtils(data).createUserFolder()
        user_serializer = UserSerializer(data=user)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        return user_serializer.data

    def register(self):
        try:
            body = self.request.data

            if (body['username'] == None or body['password'] == None or body['phone'] == None or body['email'] == None or body['name'] == None):
                raise BadRequestException("Request body fields can't be null")
        except Exception as e:
            raise BadRequestException(
                "Please check the data you sent! Required fields: Name, Username, Password, Phone, Email")
        user = FolderUtils(body).createUserFolder()
        hashed_password = make_password(user['password'])
        user['password'] = hashed_password

        try:
            user_serializer = UserSerializerForRegister(data=user)
            user_serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise BadRequestException(str(e))
        user_serializer.save()
        return "User created successfully. User id: " + str(user_serializer.data.get('id'))

    def login(self):
        username = self.request.data.get('username', None)
        password = self.request.data.get('password', None)
        if username == None or password == None:
            raise BadRequestException("Username or password can't be empty.")
        try:
            user = User.objects.get(username=username)
            serializer = UserSerializer(user)
        except User.DoesNotExist as e:
            raise BadRequestException(str(e))
        if (not user.check_password(password)):
            raise BadRequestException('Invalid username or password')

        return UserTokenResponse(serializer.data, create_access_token(user.id)).__dict__

    def uploadPhoto(self):
        user_id = self.request.query_params.get('user_id', None)
        file = self.request.data.get('file', None)
        if user_id == None or file == None:
            raise BadRequestException("File or user id can't be null.")

        file_path = FileUtils(file, user_id).moveProfilePhotoToUserFolder()
        user = User.objects.get(id=user_id)
        user.profile_photo_path = file_path
        user.save()
        serializer = UserSerializer(user)

        return serializer.data

    def getAnotherUser(self):
        user_id = self.request.query_params.get('user_id', None)

        if user_id == None:
            raise BadRequestException("User id can't be null.")

        users = User.objects.filter(~Q(id=user_id))
        serializer = UserSerializer(users, many=True)

        return serializer.data

    def heartbeat(self):
        token = self.request.data.get('token')
        try:
            user_id = decode_access_token(token)
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return UserTokenResponse(serializer.data, create_access_token(user.id)).__dict__
        except Exception as e:
            raise BadRequestException("Token expired!")
