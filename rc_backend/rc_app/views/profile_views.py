from pprint import pprint

from django.contrib.contenttypes import forms
from django.http import JsonResponse
from django.views.generic import ListView, DetailView

from rc_backend.rc_app.models import Team, Competition, CompetitionResult
from rc_backend.rc_app.models.profile import Profile


class ProfilesListView(ListView):
    model = Profile
    paginate_by = 50


def combine_profile_data(profile):
    teams_as_leader = Team.objects.filter(leader_id=profile.profile_id)
    teams_as_member = Team.objects.filter(team_members__profile_id=profile.profile_id)

    # Combine the teams
    all_teams = teams_as_leader | teams_as_member

    # Get all competitions the profile has participated in
    competitions = Competition.objects.filter(team__in=all_teams).distinct()

    # Get all competition results for these teams
    competition_results = CompetitionResult.objects.filter(team__in=all_teams).distinct()

    print(competition_results)
    # Prepare the response data
    data = {
        'teams': [{'id': str(team.team_id), 'title': team.title} for team in all_teams],
        'competitions': [{'id': str(comp.competition_id), 'title': comp.title} for comp in competitions],
        'competition_results': [
            {
                'result_id': str(result.result_id),
                'competition_id': str(result.team.competition_id),
                'team_id': str(result.team.team_id),
                'points': result.points,
                'place': result.place
            } for result in competition_results if result is not None
        ]
    }
    pprint(data)
    return data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'last_name', 'email', 'description']


class ProfileDetailView(DetailView):
    model = Profile

    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        data = combine_profile_data(profile)
        context["data"] = data
        return context
        # return render(request, self.template_name, context)


class EditProfileDetailView(DetailView):
    model = Profile

    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        data = combine_profile_data(profile)
        context["data"] = data
        return context

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Profile updated successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
