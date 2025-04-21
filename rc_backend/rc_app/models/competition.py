import uuid
from django.db import models

from . import CompetitionEnum, OnModerationStatus
from . import Team


class Competition(models.Model):
    competition_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    title = models.TextField()
    online = models.BooleanField()
    place = models.TextField(blank=True, null=True)
    description = models.TextField()
    registration_until = models.DateTimeField()
    registration_start = models.DateTimeField()
    max_participants = models.IntegerField()
    min_participants = models.IntegerField()
    competition_type = models.CharField(max_length=50, default=CompetitionEnum.NEW)
    on_moderation = models.CharField(max_length=50, default=OnModerationStatus.PENDING)
    is_shown = models.BooleanField()


class CompetitionResult(models.Model):
    result_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition_id = models.ForeignKey(Competition, on_delete=models.CASCADE)
    points = models.FloatField()
    place = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f'Result {self.result_id} - Place {self.place}'

