from rest_framework import status
from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    detail = None
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail):
        super().__init__(detail)
        self.detail = detail
