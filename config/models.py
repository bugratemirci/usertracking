from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class BaseModel(models.Model):
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ConfigValues(BaseModel):
    key = models.CharField(max_length=150)
    value = models.CharField(max_length=200)
