from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from src.core.models import Team, Competition


class TeamsForCompetitionListView(ListView):
    model = Team
    template_name = 'core/team/team/team_list.html'

    def get_queryset(self):
        competition_id = self.kwargs.get('competition_id')
        competition = get_object_or_404(Competition, id=competition_id)
        teams = Team.objects.filter(competition=competition)
        return teams
