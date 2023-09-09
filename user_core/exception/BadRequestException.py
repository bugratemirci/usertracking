from rest_framework import status
from .BaseException import BaseCustomException


class BadRequestException(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    def __init__(self, detail):
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)
