from django.contrib.auth.backends import BaseBackend
from ..models import User
from rest_framework.authentication import get_authorization_header
from ..utils.Authentication import decode_access_token


class AuthenticationBackend(BaseBackend):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if (auth and len(auth) == 2):
            if auth[0].decode() == 'Bearer':
                user_id = decode_access_token(auth[1].decode())
                
                user = User.objects.get(id=user_id)
                return [user, None]
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
