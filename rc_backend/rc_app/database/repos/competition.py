from rc_backend.rc_app.database.repos.base_repo import BaseRepo
from rc_backend.rc_app.models import Competition


class CompetitionRepo((BaseRepo[Competition])):
    model = Competition
