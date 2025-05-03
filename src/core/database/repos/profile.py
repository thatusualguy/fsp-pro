from src.core.database.repos.base_repo import BaseRepo
from src.core.models.profile import Profile


class ProfileRepo(BaseRepo[Profile]):
    model = Profile
