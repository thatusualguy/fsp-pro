from django.views.generic import ListView

from src.core.models import Region

class RegionListView(ListView):
    model = Region
    template_name = 'core/region/region_list.html'
    context_object_name = 'regions'

    def get_queryset(self):
        return Region.objects.all().order_by('name')
