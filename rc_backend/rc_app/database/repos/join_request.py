from rc_backend.rc_app.database.repos.base_repo import BaseRepo
from rc_backend.rc_app.models.join_request import JoinRequest


class JoinRequestRepo(BaseRepo[JoinRequest]):
    model = JoinRequest
