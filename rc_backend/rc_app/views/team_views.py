from pprint import pprint

from annoying.functions import get_object_or_None
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from rc_backend.rc_app.models import Team, Profile
from rc_backend.rc_app.models.invitation import TeamInvitation
from rc_backend.rc_app.models.join_request import JoinRequest
from rc_backend.rc_app.models.team import MemberSearch, CompetitionResult


##  TEAM

class TeamDetailsView(DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()

        members = team.team_members.all()
        leader = team.leader
        leader_fsp = leader.fsp
        competition = team.competition
        competition_result = get_object_or_None(CompetitionResult, team=team)

        context['members'] = members
        context['leader'] = leader
        context['competition'] = competition
        context['region'] = leader_fsp
        context['competition_result'] = competition_result
        return context


class TeamCreateView(CreateView):
    model = Team
    fields = "__all__"


class TeamUpdateView(UpdateView):
    model = Team
    fields = "__all__"


class TeamDeleteView(DeleteView):
    model = Team

    def dispatch(self, request, *args, **kwargs):
        team = self.get_object()
        # Get current user's profile
        profile = get_object_or_404(Profile, user=request.user)
        # Check if current user is the team leader
        if team.leader_id != profile:
            raise PermissionDenied("You do not have permission to delete this team.")

        return super().dispatch(request, *args, **kwargs)



## MEMBER SEARCH

class MemberSearchListView(ListView):
    model = MemberSearch
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ms = MemberSearch.objects.filter(team__competition__id=context["competition_id"])
        context['member_search'] = ms
        return context


class MemberSearchCreateView(CreateView):
    model = MemberSearch
    fields = "__all__"


class MemberSearchUpdateView(UpdateView):
    model = MemberSearch
    fields = "__all__"

    def dispatch(self, request, *args, **kwargs):
        ms: MemberSearch = self.get_object()
        # Get current user's profile
        profile = get_object_or_404(Profile, user=self.request.user)
        team = get_object_or_404(Team, team)
        # Check if current user is the team leader
        if team.leader_id != profile:
            raise PermissionDenied("You do not have permission to delete this team.")

        return super().dispatch(request, *args, **kwargs)



class MemberSearchDetailView(DetailView):
    model = MemberSearch
    fields = "__all__"



# user invited to team
class PendingTeamInvitationsListView(ListView):
    model = TeamInvitation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get Profile of the current user
        profile = Profile.objects.get(user=self.request.user)
        # Get TeamInvitations where the current user is invited
        invitations = TeamInvitation.objects.filter(invitee=profile)

        context['invitations'] = invitations
        return context


# user asks to join team

# WANNABE SIDE
class WannabePendingJoinRequestsListView(ListView):
    """request that i sent to other teams"""
    model = JoinRequest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get Profile of the current user
        profile = Profile.objects.get(user=self.request.user)
        # Get TeamInvitations where the current user is invited
        invitations = JoinRequest.objects.filter(invitee=profile)

        context['invitations'] = invitations
        return context



class WannabePendingJoinRequestCreateView(CreateView):
    model = JoinRequest



class WannabePendingJoinRequestDeleteView(DeleteView):
    model = JoinRequest


# LEADER SIDE


class LeaderPendingJoinRequestsListView(ListView):
    """request that other people have sent to my team"""
    model = JoinRequest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_id = kwargs.get("team_id")
        team = Team.objects.get(id=team_id)
        requests = JoinRequest.objects.filter(
            team=team
        )
        context['join_requests'] = requests
        return context


class LeaderPendingJoinRequestUpdateView(UpdateView):
    model = JoinRequest
    fields = ["status"]

# @force_post
# def create_team(request) -> HttpResponseRedirect:
#     name = request.POST.get("name")  # Access form field
#     competition_id = request.POST.get("competition_id")
#     leader_id = request.user.id
#
#     TeamRepo.create(
#         team_id=uuid.uuid4(),
#         title=name,
#         competition_id=competition_id,
#         leader_id=leader_id,
#         moderation_status=ModerationEnum.PENDING
#     )
#     return HttpResponseRedirect("/")
#
#
# @force_get
# def show_team(request):
#     team_id = request.GET.get("team_id")
#     model = TeamRepo.scalar(
#         team_id=team_id
#     )
#     return JsonResponse(model, safe=False)
#
#
# @force_post
# def request_to_join_team(request: HttpRequest) -> HttpResponseBadRequest | JsonResponse:
#     data = {
#         "join_id": request.POST.get("join_id") or uuid.uuid4(),
#         "team_id": request.POST.get("team_id"),
#         "profile": request.POST.get("profile"),
#         "description": request.POST.get("description"),
#         "join_status": request.POST.get("join_status"),
#     }
#
#     if not all([data["team_id"], data["profile"], data["join_status"]]):
#         return HttpResponseBadRequest("Missing required fields.")
#     JoinRequestRepo.create(**data)
#     return JsonResponse({"success": True})
#
#
# @force_post
# def create_team_invitation(request: HttpRequest) -> JsonResponse | HttpResponseBadRequest:
#     team_id = request.POST.get("inviter_team_id")
#     invitee_id = request.POST.get("invitee_id")
#
#     if not team_id or not invitee_id:
#         return HttpResponseBadRequest("Missing 'inviter_team_id' or 'invitee_id'.")
#
#     invitee = get_object_or_404(ProfileRepo.model, profile_id=invitee_id)
#
#     TeamInvitationRepo.create(
#         invitation_id=uuid.uuid4(),
#         inviter_team_id=team_id,
#         invitee=invitee,
#     )
#     return JsonResponse({"success": True})
#
#
# @force_post
# def edit_join_request(request: HttpRequest) -> JsonResponse | HttpResponseBadRequest:
#     join_id = request.POST.get("join_id")
#     join_status = request.POST.get("join_status")
#
#     if not join_id or not join_status:
#         return HttpResponseBadRequest("Missing 'join_id' or 'join_status'.")
#
#     join_model = JoinRequestRepo.scalar(join_id=join_id)
#     if join_model is None:
#         return JsonResponse({"error": "Join request not found."}, status=404)
#
#     JoinRequestRepo.update(
#         model=join_model,
#         join_status=join_status
#     )
#     return JsonResponse({"success": True})
#
#
# @force_post
# def make_team_open_for_join_requests(
#         request: HttpRequest) -> JsonResponse | HttpResponseRedirect | HttpResponseBadRequest:
#     team_id = request.POST.get("team_id")
#     desc = request.POST.get("description")
#
#     if not team_id or not desc:
#         return HttpResponseBadRequest("Missing 'team_id' or 'description' in request.")
#
#     team_model = TeamRepo.scalar(team_id=team_id)
#     if team_model is None:
#         return JsonResponse({"error": "Team not found."}, status=404)
#
#     MSRepo.create(
#         search_id=uuid.uuid4(),
#         team_id=team_model,
#         description=desc
#     )
#
#     return HttpResponseRedirect("/")
#
#
# @force_get
# def list_join_requests(request: HttpRequest) -> JsonResponse:
#     user_id = request.user.id
#
#     profile = ProfileRepo.scalar(profile_id=user_id)
#     if profile is None:
#         return JsonResponse({"error": "Profile not found"}, status=404)
#
#     teams = TeamRepo.select(leader_id=user_id).prefetch_related('joinrequest_set')
#     join_requests = []
#     for team in teams:
#         for r in team.joinrequest_set.all():
#             join_requests.append({
#                 "join_id": str(r.join_id),
#                 "team_id": str(r.team_id),
#                 "profile": str(r.profile_id),
#                 "description": r.description,
#                 "join_status": r.join_status
#             })
#
#     return JsonResponse(join_requests, safe=False)
