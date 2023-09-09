from rest_framework import status


class SuccessResponse:
    data = None
    code = status.HTTP_200_OK

    def __init__(self, data):
        self.data = data


class UserTokenResponse:
    user = None
    token = None

    def __init__(self, user, token):
        self.user = user
        self.token = token
