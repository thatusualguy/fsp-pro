import uuid

from django.db import models

from .enums import CompetitionEnum, OnModerationStatus, CompetitionTypeEnum
from .fsp import FSP


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
    competition_type = models.CharField(
        max_length=50,
        choices=CompetitionTypeEnum.choices,
        default=CompetitionTypeEnum.OPEN,
        verbose_name="Тип соревнования"
    )
    on_moderation = models.CharField(
        max_length=50,
        choices=OnModerationStatus.choices,
        default=OnModerationStatus.NEW,
        verbose_name="На модерации"
    )
    is_shown = models.BooleanField()

    fsps = models.ManyToManyField(FSP)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'
