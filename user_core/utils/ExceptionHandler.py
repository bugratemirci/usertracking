import logging

from rest_framework.views import exception_handler
from datetime import datetime
from ..exception.BadRequestException import BadRequestException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['message'] = response.data['detail']
        response.data['code'] = response.status_code
        response.data['time'] = datetime.now()
        del response.data['detail']

    return response
