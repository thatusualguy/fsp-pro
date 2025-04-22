from uuid import UUID
from rc_backend.rc_app.database.repos.base_repo import BaseRepo
from rc_backend.rc_app.models import FSP, FSPCompetition


class FSPRepo(BaseRepo[FSP]):
    model = FSP


class FSPCompetitionRepo(BaseRepo[FSPCompetition]):
    model = FSPCompetition
