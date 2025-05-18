from django.views.generic import DetailView
from src.core.models import Region


class RegionDetailView(DetailView):
    model = Region
    template_name = 'core/region_detail.html'
    context_object_name = 'region'