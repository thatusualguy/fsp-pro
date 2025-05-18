from django.urls import path

from src.core.views.regions.region_views import RegionCreateView, RegionUpdateView, RegionDeleteView, RegionListView, \
    RegionDetailView

app_name = 'regions'
urlpatterns = [
    path('', RegionListView.as_view(), name='list'),
    path('create/', RegionCreateView.as_view(), name='create'),
    path('<int:id>/', RegionDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', RegionUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', RegionDeleteView.as_view(), name='delete'),
]