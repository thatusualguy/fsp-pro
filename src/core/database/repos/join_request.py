from src.core.database.repos.base_repo import BaseRepo
from src.core.models.join_request import JoinRequest


class JoinRequestRepo(BaseRepo[JoinRequest]):
    model = JoinRequest
