from django.urls import path
from src.core.views.regions.region_views import (
    RegionListView,
    RegionDetailView,
    RegionCreateView,
    RegionUpdateView,
    RegionDeleteView,
)

app_name = 'regions'
urlpatterns = [
    path('', RegionListView.as_view(), name='list'),
    path('<int:pk>/', RegionDetailView.as_view(), name='detail'),
    path('new/', RegionCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', RegionUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', RegionDeleteView.as_view(), name='delete'),
]