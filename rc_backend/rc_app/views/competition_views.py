from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from rc_backend.rc_app.models import Competition
from rc_backend.rc_app.models.discipline import Discipline


class CompetitionListView(ListView):
    model = Competition
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        discipline_name = self.request.GET.get("discipline")
        if discipline_name:
            discipline = get_object_or_404(Discipline, discipline=discipline_name)
            queryset = queryset.filter(discipline=discipline)

        queryset = queryset.select_related("discipline")
        return queryset



class CompetitionDetailView(DetailView):
    model = Competition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        discipline = Competition.discipline
        context["discipline"] = discipline
        return context
