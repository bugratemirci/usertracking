from django.db import models


class BaseModel(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class User(BaseModel):
    name = models.CharField(max_length=80)
    username = models.CharField(max_length=80)
    phone = models.CharField(max_length=30)
    website = models.CharField(max_length=100)
    company = models.JSONField()
    address = models.JSONField()
    root_path = models.CharField(max_length=200)
    profile_photo_path = models.CharField(
        max_length=200, null=True, blank=True)


class Post(BaseModel):
    title = models.CharField(max_length=100)
    body = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)


class Comment(BaseModel):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Todo(BaseModel):
    title = models.TextField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=False)


class Photo(BaseModel):
    title = models.TextField()
    url = models.TextField()
    thumbnail_url = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Album(BaseModel):
    title = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photos = models.ManyToManyField(Photo, null=True, blank=True)
