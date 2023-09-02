import os
import environ
from ..models import User

env = environ.Env()
environ.Env.read_env()


class FileUtils:
    def __init__(self, file, user_id):
        user = User.objects.get(id=user_id)
        self.file = file
        self.user = user

    def movePhotoFileToUserFolder(self):
        file_path = os.path.join(env('USER_ROOT_PATH'),
                                 self.user.root_path, 'photos_path', self.file.name)
        if os.path.exists(file_path) != True:
            with open(file_path, 'wb+') as destinations:
                for chunk in self.file.chunks():
                    destinations.write(chunk)

            return os.path.join(self.user.root_path, 'photos_path', self.file.name)

        return None
