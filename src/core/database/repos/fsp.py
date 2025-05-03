from src.core.database.repos.base_repo import BaseRepo
from src.core.models import FSP, FSPCompetition


class FSPRepo(BaseRepo[FSP]):
    model = FSP


class FSPCompetitionRepo(BaseRepo[FSPCompetition]):
    model = FSPCompetition
