import uuid

from django.db import models

from .enums import ModerationEnum
from .profile import Profile


class Team(models.Model):
    team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    competition_id = models.UUIDField()  # Можно заменить на ForeignKey, если есть модель Competition
    leader_id = models.UUIDField()  # Можно заменить на ForeignKey, если есть модель User/Leader
    moderation_status = models.CharField(
        max_length=20,
        default=ModerationEnum.PENDING
    )

    def __str__(self):
        return self.title


# Связь команда–участник
class TeamMember(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('team_id', 'profile_id')  # составной первичный ключ

    def __str__(self):
        return f'Profile {self.profile_id} in Team {self.team_id}'
