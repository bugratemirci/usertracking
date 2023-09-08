from rest_framework import status


class SuccessResponse:
    data = None
    code = status.HTTP_200_OK

    def __init__(self, data):
        self.data = data
