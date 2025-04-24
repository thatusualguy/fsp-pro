import calendar
from collections import defaultdict
from pprint import pprint

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView

from rc_backend.rc_app.models import Competition, Team
from rc_backend.rc_app.models.discipline import Discipline


class CompetitionListView(ListView):
    model = Competition
    paginate_by = 20

    template_name = "rc_app/competition_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        discipline_name = self.request.GET.get("discipline")
        if discipline_name:
            discipline = get_object_or_404(Discipline, discipline=discipline_name)
            queryset = queryset.filter(discipline=discipline)

        queryset = queryset.select_related("discipline")

        # Group competitions by month
        competitions_by_month = defaultdict(list)
        for competition in queryset:
            month_name = _(calendar.month_name[competition.start_date.month])
            competitions_by_month[month_name].append({
                "id": competition.id,
                "day": competition.start_date.day,
                "title": competition.title,
                "url": f"/app/competition/{competition.id}/",
                "badges": [],  # Add logic for badges if needed
                "meta": competition.place,
                "event_type": "online" if competition.online else "offline",
                "event_regions": (competition.fsps.all())
            })

        data = [{"name": month, "events": events} for month, events in competitions_by_month.items()]
        pprint(data)
        return data


class CompetitionDetailView(DetailView):
    model = Competition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        discipline = Competition.discipline
        context["discipline"] = discipline
        return context


class TeamsForCompetitionListView(ListView):
    model = Team
    template_name = 'rc_app/team_list.html'

    def get_queryset(self):
        competition_id = self.kwargs.get('competition_id')
        competition = get_object_or_404(Competition, id=competition_id)
        teams = Team.objects.filter(competition=competition)
        pprint(competition)
        pprint(teams)
        pprint(teams[0].team_members.all())
        pprint(teams[0].competitionresult)
        return teams
