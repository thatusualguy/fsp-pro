from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.generic import ListView, DetailView

from rc_backend.rc_app.database.repos.competition import CompetitionRepo
from rc_backend.rc_app.database.repos.team import MSRepo, TeamRepo
from rc_backend.rc_app.models import Competition
from rc_backend.rc_app.views.utils import force_get


@force_get
def find_member_search_for_competition(request):
    competition_id = request.GET.get("competition_id")

    teams = TeamRepo.select(
        competition_id=competition_id
    )

    searches = []
    for team in teams:
        ms = MSRepo.select(
            team_id=team.id
        )
        searches.append(ms)
    return JsonResponse(searches)


class CompetitionListView(ListView):
    model = Competition
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class CompetitionDetailView(DetailView):
    model = Competition


@force_get
def get_competition_by_criteria(request):
    competition_id = request.GET.get("competition_id")
    date = request.GET.get("date")
    online = request.GET.get("online")
    sport_type = request.GET.get("sport_type")  # Assuming this is part of the model
    single = request.GET.get("single")

    filters = {}

    if competition_id:
        filters['competition_id'] = competition_id

    if date:
        parsed_date = parse_datetime(date)
        if parsed_date:
            filters['start_date__lte'] = parsed_date
            filters['finish_date__gte'] = parsed_date

    if online is not None:
        filters['online'] = online.lower() == 'true'

    if sport_type:
        filters['competition_type'] = sport_type

    if single is not None:
        filters['max_participants'] = 1 if single.lower() == 'true' else 2

    competitions = CompetitionRepo.select(**filters)

    # For simplicity, returning basic competition info as JSON
    response_data = [{
        'id': str(c.competition),
        'title': c.title,
        'start_date': c.start_date,
        'finish_date': c.finish_date,
        'online': c.online,
        'place': c.place
    } for c in competitions]
    return JsonResponse(response_data, safe=False)
