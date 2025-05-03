from src.core.database.repos.base_repo import BaseRepo
from src.core.models import InviteCompetition
from src.core.models.invitation import TeamInvitation


class InviteCompetitionRepo(BaseRepo[InviteCompetition]):
    model = InviteCompetition


class TeamInvitationRepo(BaseRepo[TeamInvitation]):
    model = TeamInvitation
