import os
import environ
from django.utils import timezone
from ..exception.BadRequestException import BadRequestException
env = environ.Env()
environ.Env.read_env()


class FolderUtils:
    def __init__(self, user):
        self.user = user

    def createUserFolder(self):
        user_folder_name = (self.user['username'].replace(
            ' ', '_').replace(':', '') + str(timezone.now().timestamp())).replace('.', '')
        path = os.path.join(env('USER_ROOT_PATH'),
                            user_folder_name)
        try:
            os.mkdir(path)
            videos_path = os.path.join(path, 'video_path')
            photos_path = os.path.join(path, 'photos_path')
            os.mkdir(videos_path)
            os.mkdir(photos_path)
            self.user['root_path'] = user_folder_name
            return self.user
        except Exception as error:
            raise BadRequestException("User root path exists.")
