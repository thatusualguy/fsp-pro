from django.views.generic import ListView, DetailView
from rc_backend.rc_app.models import Competition


class CompetitionListView(ListView):
    model = Competition
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        discipline = Competition.discipline
        context["discipline"] = discipline
        return context


class CompetitionDetailView(DetailView):
    model = Competition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        discipline = Competition.discipline
        context["discipline"] = discipline
        return context
