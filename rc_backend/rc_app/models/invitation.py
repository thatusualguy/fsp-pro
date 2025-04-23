# InviteCompetition Model
import uuid

from django.db import models

from .competition import Competition
from .enums import TeamInvitationEnum, InviteStatusEnum
from .fsp import FSP
from .profile import Profile
from .team import Team


class InviteCompetition(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    invitee = models.ForeignKey(FSP, on_delete=models.CASCADE,
                                related_name='invites_received')
    inviter = models.ForeignKey(FSP, on_delete=models.CASCADE,
                                related_name='invites_sent')
    creation_stamp = models.DateTimeField(auto_now_add=True)  # timestamp
    competition_id = models.ForeignKey(Competition, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        default=InviteStatusEnum.PENDING
    )

    def __str__(self):
        return f"Invite {self.id} - {self.status}"

    class Meta:
        verbose_name = 'Приглашение соревнование'
        verbose_name_plural = 'Приглашения на соревнования'


class TeamInvitation(models.Model):
    invitation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inviter_team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    invitee = models.ForeignKey(Profile, on_delete=models.CASCADE)
    invitation_status = models.CharField(
        max_length=20,
        default=TeamInvitationEnum.PENDING
    )

    def __str__(self):
        return f'Invitation {self.invitation_id} to {self.invitee}'
