import uuid

from django.db import models

from .competition import Competition
from .enums import ModerationEnum
from .profile import Profile


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    competition = models.ForeignKey(Competition,
                                    on_delete=models.CASCADE)  # Можно заменить на ForeignKey, если есть модель Competition
    leader = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='leader_teams')
    team_members = models.ManyToManyField(Profile, related_name='member_teams')

    moderation_status = models.CharField(
        max_length=20,
        choices=ModerationEnum.choices,
        default=ModerationEnum.PENDING,
        verbose_name='Статус модерации'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'


class CompetitionResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # competition_id = models.ForeignKey(Competition, on_delete=models.CASCADE)
    points = models.FloatField()
    place = models.IntegerField()
    team = models.OneToOneField(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f'Result {self.id} - Place {self.place}'


class MemberSearch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Search {self.id} for Team {self.team}"
