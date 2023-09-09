from django.contrib.auth.backends import BaseBackend
from ..models import User
from rest_framework.authentication import get_authorization_header
from ..utils.Authentication import decode_access_token
from ..exception.BadRequestException import BadRequestException


class AuthenticationBackend(BaseBackend):
    def authenticate(self, request):
        base_url = 'http://localhost:8000/'
        allowed_uris = [base_url + 'users/login/',
                        base_url + 'users/register/',
                        base_url + 'swagger/',
                        base_url + 'swagger/?format=openapi',
                        base_url + 'redoc/',
                        base_url + 'redoc/?format=openapi',
                        base_url + 'users/heartbeat/']
        try:
            if len(get_authorization_header(request).split()) == 0 and request.build_absolute_uri() not in allowed_uris:
                raise BadRequestException("Authorization not found in request")
            auth = get_authorization_header(request).split()
            if (auth and len(auth) == 2):
                if auth[0].decode() == 'Bearer':

                    user_id = decode_access_token(auth[1].decode())
                    user = User.objects.get(id=user_id)
                    return [user, None]
        except Exception as e:
            raise BadRequestException(e.detail)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise BadRequestException("User does not exists.")
