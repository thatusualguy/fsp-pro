from annoying.functions import get_object_or_None
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, DeleteView, ListView

from src.core.models import Team, Profile
from src.core.models.enums import ModerationEnum
from src.core.models.team import CompetitionResult


class MyTeamsListView(ListView):
    model = Team
    template_name = "core/team/team/team_list.html"

    def get_queryset(self):
        member_teams = self.request.user.profile.member_teams.all()
        leader_teams = self.request.user.profile.leader_teams.all()
        return member_teams | leader_teams


class TeamDetailsView(DetailView):
    model = Team
    template_name = "core/team/team/team_detail.html"

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
        context['now'] = timezone.now()
        context["show_send"] = team.moderation_status == ModerationEnum.NOT_SENT
        context['competition'] = competition
        context['is_member'] = self.request.user.profile in team.team_members.all()
        context['region'] = leader_fsp
        context['competition_result'] = competition_result
        return context


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
