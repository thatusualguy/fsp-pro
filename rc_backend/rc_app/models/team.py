import uuid

from django.db import models

from .competition import Competition
from .enums import ModerationEnum
from .profile import Profile



class Team(models.Model):
    team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    competition_id =  models.ForeignKey(Competition, on_delete=models.CASCADE)  # Можно заменить на ForeignKey, если есть модель Competition
    leader_id = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Можно заменить на ForeignKey, если есть модель User/Leader

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


class TeamMember(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('team_id', 'profile_id')  # составной первичный ключ

    def __str__(self):
        return f'Profile {self.profile_id} in Team {self.team_id}'


class CompetitionResult(models.Model):
    result_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition_id = models.ForeignKey(Competition, on_delete=models.CASCADE)
    points = models.FloatField()
    place = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f'Result {self.result_id} - Place {self.place}'


class MemberSearch(models.Model):
    search_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team_id = models.ForeignKey(to=Team, on_delete=models.CASCADE)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Search {self.search_id} for Team {self.team_id}"