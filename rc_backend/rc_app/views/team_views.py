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

    def dispatch(self, request, *args, **kwargs):
        team: Team = self.get_object()
        # Get current user's profile
        profile = get_object_or_404(Profile, user=self.request.user)

        # Check if current user is the team leader
        if team.leader != profile:
            raise PermissionDenied("You do not have permission to update this team.")

        return super().dispatch(request, *args, **kwargs)


class TeamDeleteView(DeleteView):
    model = Team

    def dispatch(self, request, *args, **kwargs):
        team: Team = self.get_object()
        # Get current user's profile
        profile = get_object_or_404(Profile, user=request.user)
        # Check if current user is the team leader
        if team.leader != profile:
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

    def dispatch(self, request, *args, **kwargs):
        ms: MemberSearch = self.get_object()
        # Get current user's profile
        profile = get_object_or_404(Profile, user=self.request.user)
        team: Team = ms.team

        # Check if current user is the team leader
        if team.leader != profile:
            raise PermissionDenied("You do not have permission to create member search.")
        return super().dispatch(request, *args, **kwargs)


class MemberSearchUpdateView(UpdateView):
    model = MemberSearch
    fields = "__all__"

    def dispatch(self, request, *args, **kwargs):
        ms: MemberSearch = self.get_object()
        # Get current user's profile
        profile = get_object_or_404(Profile, user=self.request.user)
        team = ms.team

        # Check if current user is the team leader
        if team.leader != profile:
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

    def dispatch(self, request, *args, **kwargs):
        join_request: JoinRequest = self.get_object()
        profile = get_object_or_404(Profile, user=self.request.user)
        team: Team = join_request.team
        leader: Profile = team.leader

        # Check if current user is the team leader
        if leader.fsp != profile.fsp:
            raise PermissionDenied("You do not have permission to join this team.")
        return super().dispatch(request, *args, **kwargs)


class WannabePendingJoinRequestDeleteView(DeleteView):
    model = JoinRequest

    def dispatch(self, request, *args, **kwargs):
        join_request: JoinRequest = self.get_object()
        profile = get_object_or_404(Profile, user=self.request.user)

        # Check if current user is the team leader
        if profile != join_request.profile:
            raise PermissionDenied("You do not have permission to delete this join request.")
        return super().dispatch(request, *args, **kwargs)


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

    def dispatch(self, request, *args, **kwargs):
        join_request: JoinRequest = self.get_object()
        team = join_request.team
        profile = get_object_or_404(Profile, user=self.request.user)

        # Check if current user is the team leader
        if team.leader != profile:
            raise PermissionDenied("You do not have permission to delete this team.")
        return super().dispatch(request, *args, **kwargs)

