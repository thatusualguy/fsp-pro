from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from src.core.models import Region


class RegionDetailView(DetailView):
    model = Region
    template_name = 'core/region/region_detail.html'
    context_object_name = 'region'
    slug_field = 'code'  # Поле модели для поиска
    slug_url_kwarg = 'code'

    def get_object(self, queryset=None):
        return get_object_or_404(Region, code=self.kwargs['code'])