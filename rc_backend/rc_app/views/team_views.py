import json
import uuid
from functools import wraps

from rc_backend.rc_app.database.repos.invitation import TeamInvitationRepo
from rc_backend.rc_app.database.repos.join_request import JoinRequestRepo
from rc_backend.rc_app.database.repos.profile import ProfileRepo
from rc_backend.rc_app.database.repos.team import TeamRepo, MSRepo
from rc_backend.rc_app.models import ModerationEnum
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseRedirect

from rc_backend.rc_app.views.utils import force_post, force_get


@force_post
def create_team(request):
    name = request.POST.get("name")  # Access form field
    competition_id = request.POST.get("competition_id")
    leader_id = request.user.id

    TeamRepo.create(
        team_id=uuid.uuid4(),
        title=name,
        competition_id=competition_id,
        leader_id=leader_id,
        moderation_status=ModerationEnum.PENDING
    )

@force_get
def show_team(request):
    team_id = request.GET.get("team_id")
    model = TeamRepo.scalar(
        team_id=team_id
    )
    return HttpResponse(content=json.dumps(model))


# class JoinRequest(BaseModel):
#     join_id: int
#     team_id: int
#     profile: str
#     description: Optional[str] = None
#     join_status: Optional[str] = None
@force_post
def request_to_join_team(request):
    join_id = request.POST.get("join_id")
    team_id = request.POST.get("team_id")
    profile = request.POST.get("profile")
    description = request.POST.get("description")
    join_status = request.POST.get("join_status")

    JoinRequestRepo.create(
        join_id=join_id,
        team_id=team_id,
        profile=profile,
        description=description,
        join_status=join_status
    )
    return HttpResponseRedirect("/")


@force_post
def create_team_invitation(request):
    team_id = request.POST.get("inviter_team_id")
    invitee_id = request.POST.get("invitee_id")

    invitee = ProfileRepo.scalar(
        profile_id=invitee_id
    )
    TeamInvitationRepo.create(
        invitation_id=uuid.uuid4(),
        inviter_team_id=team_id,
        invitee=invitee,
    )
    return HttpResponseRedirect("/")


@force_post
def edit_join_request(request):
    join_id = request.POST.get("join_id")
    join_status = request.POST.get("join_status")

    join_model = JoinRequestRepo.scalar(
        join_id=join_id
    )
    JoinRequestRepo.update(
        model=join_model,
        join_status=join_status
    )
    return HttpResponseRedirect("/")


@force_post
def make_team_open_for_join_requests(request):
    team_id = request.POST.get("team_id")
    desc = request.POST.get("description")

    team_model = TeamRepo.scalar(
        team_id=team_id
    )
    if team_model is None:
        pass

    MSRepo.create(
        search_id=uuid.uuid4(),
        team_id=team_model,
        description=desc
    )
    return HttpResponseRedirect("/")


@force_get
def list_join_requests(request):
    user_id = request.user.id
    profile = ProfileRepo.scalar(
        profile_id=user_id
    )
    if profile is None:
        pass

    teams = TeamRepo.select(

        leader_id=user_id
    )
    jr = []
    for team in teams:
        jr.append(
            JoinRequestRepo.scalar(
            team_id=team.team_id)
        )
    return HttpResponse(json.dumps(jr))



