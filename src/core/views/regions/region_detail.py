from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from src.core.models import Region


class RegionDetailView(DetailView):
    model = Region
    template_name = 'core/region/region_detail.html'
    context_object_name = 'region'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Region.objects.all()