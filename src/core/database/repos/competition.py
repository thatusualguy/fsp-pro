from src.core.database.repos.base_repo import BaseRepo
from src.core.models import Competition


class CompetitionRepo((BaseRepo[Competition])):
    model = Competition
