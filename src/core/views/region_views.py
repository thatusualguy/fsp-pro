from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from src.core.models import Region


class RegionListView(ListView):
    model = Region
    template_name = 'core/region/region_list.html'
    context_object_name = 'regions'
    ordering = ['name']

class RegionDetailView(DetailView):
    model = Region
    template_name = 'core/region/region_detail.html'
    context_object_name = 'region'

class RegionCreateView(SuccessMessageMixin, CreateView):
    model = Region
    template_name = 'core/region/region_form.html'
    fields = ['name', 'federal_district', 'timezone', 'population', 'code']
    success_url = reverse_lazy('region-list')
    success_message = "Регион успешно создан"

class RegionUpdateView(SuccessMessageMixin, UpdateView):
    model = Region
    template_name = 'core/region/region_form.html'
    fields = ['name', 'federal_district', 'timezone', 'population', 'code']
    success_url = reverse_lazy('region-list')
    success_message = "Регион успешно обновлен"

class RegionDeleteView(DeleteView):
    model = Region
    template_name = 'core/region/region_confirm_delete.html'
    success_url = reverse_lazy('region-list')
    success_message = "Регион успешно удален"