from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class BaseModel(models.Model):
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=80)
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=30)
    website = models.CharField(max_length=100, null=True, blank=True)
    company = models.JSONField(null=True, blank=True)
    address = models.JSONField(null=True, blank=True)
    root_path = models.CharField(max_length=200)
    profile_photo_path = models.CharField(
        max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()


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
