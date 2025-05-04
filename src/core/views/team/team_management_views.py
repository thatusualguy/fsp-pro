from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View

from src.core.models import Team


class TeamLeaveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        team_id = kwargs.get('team_id')
        profile = request.user.profile
        team = get_object_or_404(Team, id=team_id)

        if team.leader == profile:
            raise PermissionDenied("The leader cannot leave the team. Please assign a new leader before leaving.")

        if team.competition.registration_until < timezone.now():
            raise PermissionDenied("You cannot leave after registration end.")

        if profile in team.team_members.all():
            team.team_members.remove(profile)
        else:
            raise PermissionDenied("You are not a member of this team.")

        return HttpResponseRedirect(reverse('core:my_teams_list'))


class DisbandTeamView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        team = Team.objects.get(id=kwargs['team_id'])
        profile = request.user.profile

        if team.leader != profile:
            raise PermissionDenied("You do not have permission to disband this team.")

        if team.competition.registration_until > timezone.now():
            raise PermissionDenied("Too late.")

        team.disband()
        return redirect('core:my_teams_list')
