from datetime import datetime
from django.shortcuts import get_object_or_404
import calendar
from collections import defaultdict
from pprint import pprint
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView
from rc_backend.rc_app.models import Competition, Team
from rc_backend.rc_app.models.discipline import Discipline


def prepare_competition_data(queryset):
    """
    Processes a queryset of Competition objects and returns data
    grouped by month in the desired JSON structure.
    """

    grouped_events = defaultdict(list)

    # --- Set Locale for Russian Month Names ---
    # Ensure 'ru_RU.UTF-8' or similar is installed on your system
    # --- Iterate and Group Competitions ---
    for competition in queryset:
        if not competition.start_date:
            continue  # Skip competitions without a start date

        # Use YYYY-MM for reliable sorting key
        month_key = competition.start_date.strftime('%Y-%m')

        # --- Prepare Badges (Example Logic - ADAPT TO YOUR MODEL FIELDS) ---
        badges = []
        if competition.online:
            badges.append({"text": "Онлайн", "type": "type-online"})
        else:
            badges.append({"text": "Офлайн", "type": "type-offline"})

        # Example: Add registration status badge based on other model fields
        # if competition.registration_status == 'open':
        #     badges.append({"text": "Идет регистрация", "type": "status-registration"})
        # elif competition.registration_status == 'soon':
        #      badges.append({"text": "Скоро", "type": "status-soon"})
        # elif competition.registration_status == 'closed':
        #     badges.append({"text": "Регистрация закрыта", "type": "status-closed"})

        # --- Determine Event Region Slug (Example Logic - ADAPT) ---
        # !!! This needs proper logic based on your 'fsps' relation or 'place' field !!!
        event_region_slug = 'all'  # Default
        if not competition.online:
            # Example 1: Use the first related 'fsp' slug if available
            # related_fsps = competition.fsps.all()
            # if related_fsps.exists():
            #     event_region_slug = related_fsps.first().slug # Assuming 'slug' field exists
            # Example 2: Map 'place' text (less reliable)
            if competition.place:
                place_lower = competition.place.lower()
                if 'москва' in place_lower:
                    event_region_slug = 'msk'
                elif 'санкт-петербург' in place_lower:
                    event_region_slug = 'spb'
                # Add more mappings...
                else:
                    event_region_slug = 'other'  # Or keep 'all'?
            else:
                event_region_slug = 'unknown'  # Or 'other'?

        # --- Build Event Dictionary for the current competition ---
        event_data = {
            # "id": competition.slug if hasattr(competition, 'slug') else competition.id, # Use slug if available
            "id": competition.id,  # Using integer ID as per original code
            "day": competition.start_date.day,
            "date_start": competition.start_date,
            "date_end": competition.finish_date,
            "title": competition.title,
            "url": f"/app/competition/{competition.id}/",  # Consider using reverse()
            # "url": reverse('competition_detail', args=[competition.slug or competition.id]),
            "badges": badges,
            "meta": competition.place if not competition.online else None,  # Show place only for offline
            "event_type": "online" if competition.online else "offline",
            "event_region": event_region_slug,
            # Note: "event_regions" from previous code is mapped to a single "event_region" slug now
        }
        grouped_events[month_key].append(event_data)

    # --- Convert grouped data to the final sorted list format ---
    competitions_by_month_final = []
    # Sort by year-month key ('YYYY-MM') to ensure chronological order
    for month_key in sorted(grouped_events.keys()):
        year, month_num = map(int, month_key.split('-'))
        # Get localized month name using the set locale
        # month_name = _(calendar.month_name[month_num]).capitalize() # If using Django translation
        month_name = calendar.month_name[month_num].capitalize()
        competitions_by_month_final.append({
            "name": month_name,
            "events": grouped_events[month_key]  # Add the list of events for this month
        })

    # --- Final data structure ---
    data = {"competitions_by_month": competitions_by_month_final}
    # from pprint import pprint # Uncomment for debugging
    # pprint(data)
    return data

import calendar
from collections import defaultdict
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
# from django.utils.translation import gettext as _ # Если используете перевод
# from .models import Competition, Discipline # Импорт моделей
# from .utils import prepare_competition_data # Импорт вашей функции обработки
from pprint import pprint # Для отладки

class CompetitionListView(ListView):
    model = Competition
    template_name = "rc_app/competition_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        # === Фильтрация по дисциплине ===
        discipline_name = self.request.GET.get("discipline")
        if discipline_name:
            try:
                discipline = Discipline.objects.get(discipline__iexact=discipline_name)
                queryset = queryset.filter(discipline=discipline)
            except Discipline.DoesNotExist:
                queryset = queryset.none()

        # === Фильтрация по типу (online/offline) ===
        competition_type = self.request.GET.get("type", "all")
        if competition_type == "online":
            queryset = queryset.filter(online=True)
        elif competition_type == "offline":
            queryset = queryset.filter(online=False)

        # === Фильтрация по региону ===
        region = self.request.GET.get("region", "all")
        if region != "all":
            if region == "msk":
                queryset = queryset.filter(place__icontains="Москва")
            elif region == "spb":
                queryset = queryset.filter(place__icontains="Петербург") | queryset.filter(place__icontains="Санкт-Петербург")
                # Можно добавить другие регионы по необходимости

        # === Фильтрация по дате: выбранная дата попадает в диапазон start_date..end_date ===
        date_from_str = self.request.GET.get("date_from")

        if date_from_str:
            try:
                date_from = datetime.strptime(date_from_str, "%Y-%m-%d")
                pprint(date_from)
                start_date = datetime(date_from.year, date_from.month, date_from.day + 1, 23, 59)
                end_date = datetime(date_from.year, date_from.month, date_from.day + 1, 0, 0)
                print(start_date)
                print(end_date)
                # Важно: делаем фильтр "start_date <= date_from <= end_date"
                queryset = queryset.filter(start_date__lte=start_date, finish_date__gte=end_date)
            except ValueError:
                pass  # Некорректная дата — игнорируем фильтр

        queryset = queryset.select_related("discipline").prefetch_related("fsps").only(
            "id", "title", "start_date", "finish_date", "online", "place",
            "discipline__discipline",
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        competitions = context.get('object_list')

        if competitions is not None:
            processed_data = prepare_competition_data(list(competitions))
            context['competitions_by_month'] = processed_data.get('competitions_by_month', [])
        else:
            context['competitions_by_month'] = []

        # Список дисциплин для выпадающего списка
        all_disciplines = Discipline.objects.all()

        # Забираем все нужные фильтры из запроса
        context['competitions_data'] = {
             'current_filters': {
                 'type': self.request.GET.get('type', 'all'),
                 'region': self.request.GET.get('region', 'all'),
                 'discipline': self.request.GET.get('discipline', None),
                 'date_from': self.request.GET.get('date_from', None),
             }
        }
        context['disciplines'] = all_disciplines
        pprint(context)
        return context



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
