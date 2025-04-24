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
    # paginate_by = 10 # Пример пагинации (раскомментируйте, если нужно)
    template_name = "rc_app/competition_list.html"
    # context_object_name = 'competition_list' # Можно задать имя переменной в шаблоне, если нужно

    def get_queryset(self):
        """
        Этот метод должен возвращать ТОЛЬКО QuerySet.
        Фильтрация и оптимизация - здесь.
        """
        # Получаем базовый queryset (обычно Competition.objects.all())
        queryset = super().get_queryset() # Пример: выбираем только активные

        # Применяем фильтр по дисциплине, если он есть в GET параметрах
        discipline_name = self.request.GET.get("discipline")
        if discipline_name:
            # Безопаснее использовать get_object_or_404 или обрабатывать DoesNotExist
            try:
                discipline = Discipline.objects.get(discipline__iexact=discipline_name) # Поиск без учета регистра
                queryset = queryset.filter(discipline=discipline)
            except Discipline.DoesNotExist:
                # Можно вернуть пустой queryset или оставить как есть (будет все)
                queryset = queryset.none() # Вернуть пустой, если дисциплина не найдена

        # Оптимизируем запросы к связанным моделям
        # Указываем 'discipline' и 'fsps', если они нужны в prepare_competition_data
        queryset = queryset.select_related("discipline").prefetch_related("fsps")

        # Оптимизируем поля, чтобы не тянуть лишнее из БД (опционально)
        queryset = queryset.only(
            "id", "title", "start_date", "online", "place",
            "discipline__discipline", # Пример доступа к полю связанной модели
             # Добавьте сюда поля, необходимые для логики event_regions/badges
             # "registration_status", ...
             # Не указывайте 'fsps' здесь, т.к. используется prefetch_related
        )

        # Просто возвращаем QuerySet
        print("DEBUG: Queryset generated") # Отладка
        return queryset

    def get_context_data(self, **kwargs):
        """
        Здесь мы получаем базовый контекст и ДОБАВЛЯЕМ обработанные данные.
        """
        # Получаем базовый контекст от ListView (уже будет содержать object_list/competition_list)
        context = super().get_context_data(**kwargs)

        # Получаем уже отфильтрованный и готовый к использованию список объектов
        # Имя ('object_list' или 'competition_list') зависит от context_object_name или модели
        competitions = context.get('object_list') # По умолчанию 'object_list'

        if competitions is not None:
            # Вызываем нашу функцию обработки для данных, УЖЕ ПОЛУЧЕННЫХ из БД
            # Передаем сам список объектов, а не queryset, чтобы не бить БД снова
            processed_data = prepare_competition_data(list(competitions))

            # Добавляем нужную часть обработанных данных в контекст
            context['competitions_by_month'] = processed_data.get('competitions_by_month', [])

            # Можно добавить и другие ключи из processed_data, если они нужны
            # context['some_other_processed_key'] = processed_data.get('some_key')

            # Отладка: Печатаем финальный контекст (часть данных)
            print("--- DEBUG: Processed context data ---")
            pprint(context.get('competitions_by_month', [])[:1]) # Печатаем только первый месяц
            print("--- End DEBUG context ---")

        else:
            # Если competitions is None (маловероятно в ListView, но на всякий случай)
            context['competitions_by_month'] = []
            print("WARNING: 'object_list' not found in context.")

        # Добавляем данные о текущих фильтрах для подсветки в шаблоне
        # Это лучше делать здесь, а не внутри prepare_competition_data
        context['competitions_data'] = {
             'current_filters': {
                 'type': self.request.GET.get('type', 'all'), # Пример
                 'region': self.request.GET.get('region', 'all'), # Пример
                 'discipline': self.request.GET.get('discipline', None)
             }
         }

        # Возвращаем обновленный контекст для рендеринга шаблона
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
