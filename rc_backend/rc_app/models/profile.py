import uuid

from django.contrib.auth.models import User
from django.db import models

from rc_backend.rc_app.models import FSP


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    description = models.TextField(blank=True, null=True)
    fsp = models.ForeignKey(FSP, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.last_name}'
