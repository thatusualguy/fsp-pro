from django.db import models

from .competition import Competition


# Define the StrEnum for status field

# FSP Model
class FSP(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    region = models.CharField(max_length=255)  # str
    country = models.CharField(max_length=255)  # str
    head = models.CharField(max_length=255)  # str
    head_email = models.EmailField()  # str (EmailField for validation)
    is_federal = models.BooleanField()  # bool

    def __str__(self):
        return f"{self.head} ({self.region})"


# FSPCompetition Model
class FSPCompetition(models.Model):
    fsp_id = models.ForeignKey(
        FSP,
        on_delete=models.CASCADE,
        related_name='fsp_competitions'
    )
    competition_id = models.ForeignKey(Competition, on_delete=models.CASCADE)
