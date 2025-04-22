from rc_backend.rc_app.database.repos.base_repo import BaseRepo
from rc_backend.rc_app.models import InviteCompetition
from rc_backend.rc_app.models.invitation import TeamInvitation


class InviteCompetitionRepo(BaseRepo[InviteCompetition]):
    model = InviteCompetition


class TeamInvitationRepo(BaseRepo[TeamInvitation]):
    model = TeamInvitation
