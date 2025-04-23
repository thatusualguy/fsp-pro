import uuid

from django.db import models
from tweepy import User


# Define the StrEnum for status field

# FSP Model
class FSP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    region = models.CharField(max_length=255)  # str
    country = models.CharField(max_length=255)  # str
    head = models.OneToOneField(User, on_delete=models.CASCADE)  # str
    head_email = models.EmailField()  # str (EmailField for validation)
    is_federal = models.BooleanField()  # bool

    def __str__(self):
        return f"{self.head} ({self.region})"

    class Meta:
        verbose_name = 'Региональная ФСП'
        verbose_name_plural = 'Региональные ФСП'
