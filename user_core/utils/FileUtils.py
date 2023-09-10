import os
import environ
from ..models import User
from ..exception.BadRequestException import BadRequestException
env = environ.Env()
environ.Env.read_env()


class FileUtils:
    def __init__(self, file, user_id):
        if file != -1 and user_id != -1:
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
        else:
            raise BadRequestException("File exists.")

    def moveProfilePhotoToUserFolder(self):
        file_path = os.path.join(env('USER_ROOT_PATH'),
                                 self.user.root_path, self.file.name)

        if (os.path.exists(file_path) != True):
            with open(file_path, 'wb+') as destinations:
                for chunk in self.file.chunks():
                    destinations.write(chunk)
            return os.path.join(self.user.root_path, self.file.name)
        else:
            raise BadRequestException("File exists.")

    def removePhoto(self, photo_path):
        file_path = env('USER_ROOT_PATH')
        print(file_path + "/" + photo_path)
        if (os.path.exists(file_path + "/" + photo_path)):
            os.remove(file_path + "/" + photo_path)
