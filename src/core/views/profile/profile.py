from pprint import pprint

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView

from src.core.models import Team, Competition, CompetitionResult, FSP
from src.core.models.profile import Profile


def combine_profile_data(profile):
    teams_as_leader = Team.objects.filter(leader_id=profile.id)
    teams_as_member = Team.objects.filter(team_members__id=profile.id)

    # Combine the teams
    all_teams = teams_as_leader | teams_as_member

    # Get all competitions the profile has participated in
    competitions = Competition.objects.filter(team__in=all_teams).distinct()

    # Get all competition results for these teams
    competition_results = CompetitionResult.objects.filter(team__in=all_teams).distinct()

    print(competition_results)
    # Prepare the response data
    data = {
        'teams': all_teams,
        'competitions': competitions,
        'competition_results': [
            {
                'result_id': str(result.id),
                'competition_id': str(result.team.competition.id),
                'competition_name': str(result.team.competition.title),
                'team_id': str(result.team.id),
                'team_title': str(result.team.title),
                'points': result.points,
                'place': result.place
            } for result in competition_results if result is not None
        ]
    }
    pprint(data)
    return data



class MyProfileDetailView(DetailView):
    model = Profile
    template_name = 'core/profile/profile_detail.html'

    def get_object(self, queryset=None):
        # Return the profile of the currently logged-in user
        return self.request.user.profile

    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        data = combine_profile_data(profile)
        context["data"] = data
        # pprint(context)
        return context


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "core/profile/profile_detail.html"

    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        data = combine_profile_data(profile)
        context["data"] = data
        # pprint(context)
        return context
        # return render(request, self.template_name, context)


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['name', 'last_name', 'email', 'description', 'fsp']
    success_url = reverse_lazy('core:profile')
    template_name = "core/profile/profile_edit.html"
    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context["fsps"] = FSP.objects.all()

        return context


