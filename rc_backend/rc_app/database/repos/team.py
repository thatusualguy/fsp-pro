from rc_backend.rc_app.database.repos.base_repo import BaseRepo
from rc_backend.rc_app.models import Team
from rc_backend.rc_app.models.team import MemberSearch


class TeamRepo(BaseRepo[Team]):
    model = Team


class MSRepo(BaseRepo[MemberSearch]):
    model = MemberSearch