import json
import uuid
from functools import wraps

from rc_backend.rc_app.database.repos.invitation import TeamInvitationRepo
from rc_backend.rc_app.database.repos.join_request import JoinRequestRepo
from rc_backend.rc_app.database.repos.profile import ProfileRepo
from rc_backend.rc_app.database.repos.team import TeamRepo, MSRepo
from rc_backend.rc_app.models import ModerationEnum
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse, \
    HttpResponseBadRequest

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


@force_post
def request_to_join_team(request: HttpRequest) -> JsonResponse:
    data = {
        "join_id": request.POST.get("join_id") or uuid.uuid4(),
        "team_id": request.POST.get("team_id"),
        "profile": request.POST.get("profile"),
        "description": request.POST.get("description"),
        "join_status": request.POST.get("join_status"),
    }

    if not all([data["team_id"], data["profile"], data["join_status"]]):
        return HttpResponseBadRequest("Missing required fields.")
    JoinRequestRepo.create(**data)
    return JsonResponse({"success": True})


@force_post
def create_team_invitation(request: HttpRequest) -> JsonResponse:
    team_id = request.POST.get("inviter_team_id")
    invitee_id = request.POST.get("invitee_id")

    if not team_id or not invitee_id:
        return HttpResponseBadRequest("Missing 'inviter_team_id' or 'invitee_id'.")

    invitee = ProfileRepo.scalar(profile_id=invitee_id)
    if invitee is None:
        return JsonResponse({"error": "Invitee not found."}, status=404)

    TeamInvitationRepo.create(
        invitation_id=uuid.uuid4(),
        inviter_team_id=team_id,
        invitee=invitee,
    )
    return JsonResponse({"success": True})


@force_post
def edit_join_request(request: HttpRequest) -> JsonResponse:
    join_id = request.POST.get("join_id")
    join_status = request.POST.get("join_status")

    if not join_id or not join_status:
        return HttpResponseBadRequest("Missing 'join_id' or 'join_status'.")

    join_model = JoinRequestRepo.scalar(join_id=join_id)
    if join_model is None:
        return JsonResponse({"error": "Join request not found."}, status=404)

    JoinRequestRepo.update(
        model=join_model,
        join_status=join_status
    )
    return JsonResponse({"success": True})


@force_post
def make_team_open_for_join_requests(request: HttpRequest) -> HttpResponseRedirect | JsonResponse:
    team_id = request.POST.get("team_id")
    desc = request.POST.get("description")

    if not team_id or not desc:
        return HttpResponseBadRequest("Missing 'team_id' or 'description' in request.")

    team_model = TeamRepo.scalar(team_id=team_id)
    if team_model is None:
        return JsonResponse({"error": "Team not found."}, status=404)

    MSRepo.create(
        search_id=uuid.uuid4(),
        team_id=team_model,
        description=desc
    )

    return HttpResponseRedirect("/")


@force_get
def list_join_requests(request: HttpRequest) -> JsonResponse:
    user_id = request.user.id

    profile = ProfileRepo.scalar(profile_id=user_id)
    if profile is None:
        return JsonResponse({"error": "Profile not found"}, status=404)

    teams = TeamRepo.select(leader_id=user_id)
    join_requests = []
    for team in teams:
        requests = JoinRequestRepo.select(team_id=team.team_id)
        for r in requests:
            join_requests.append({
                "join_id": str(r.join_id),
                "team_id": str(r.team_id),
                "profile": str(r.profile_id),
                "description": r.description,
                "join_status": r.join_status
            })

    return JsonResponse(join_requests, safe=False)



