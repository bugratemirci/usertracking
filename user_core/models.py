from django.db import models
import uuid
# Create your models here.


class BaseModel(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class User(BaseModel):
    name = models.CharField(max_length=80)
    username = models.CharField(max_length=80)
    phone = models.CharField(max_length=30)
    website = models.CharField(max_length=100)
    company = models.JSONField()
    address = models.JSONField()
