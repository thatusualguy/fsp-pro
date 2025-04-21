from django.db import models
from rc_backend.rc_app.models.enums import RoleEnum


class Profile(models.Model):
    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    role = models.CharField(
        max_length=20,
        default=RoleEnum.MEMBER
    )
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} {self.last_name}'