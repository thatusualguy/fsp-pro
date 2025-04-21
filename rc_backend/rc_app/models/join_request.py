import uuid
from django.db import models

from rc_backend.rc_app.models import Team
from rc_backend.rc_app.models.enums import JoinRequestEnum
from rc_backend.rc_app.models.profile import Profile


class JoinRequest(models.Model):
    join_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField()
    join_status = models.CharField(
        max_length=20,
        default=JoinRequestEnum.PENDING
    )

    def __str__(self):
        return f'JoinRequest by {self.profile} to team {self.team_id}'