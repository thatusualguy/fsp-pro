from src.core.database.repos.base_repo import BaseRepo
from src.core.models import Team
from src.core.models.team import MemberSearch


class TeamRepo(BaseRepo[Team]):
    model = Team


class MSRepo(BaseRepo[MemberSearch]):
    model = MemberSearch
