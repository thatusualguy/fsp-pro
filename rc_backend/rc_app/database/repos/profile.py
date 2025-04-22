from rc_backend.rc_app.database.repos.base_repo import BaseRepo
from rc_backend.rc_app.models.join_request import JoinRequest
from rc_backend.rc_app.models.profile import Profile


class ProfileRepo(BaseRepo[Profile]):
    model = Profile
