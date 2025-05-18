from django.urls import path
from .views.region_views import (
    RegionListView,
    RegionDetailView,
    RegionCreateView,
    RegionUpdateView,
    RegionDeleteView,
)


app_name = "core"
urlpatterns = [
    # Region URLs
    path('regions/', RegionListView.as_view(), name='region-list'),
    path('regions/<int:pk>/', RegionDetailView.as_view(), name='region-detail'),
    path('regions/new/', RegionCreateView.as_view(), name='region-create'),
    path('regions/<int:pk>/edit/', RegionUpdateView.as_view(), name='region-update'),
    path('regions/<int:pk>/delete/', RegionDeleteView.as_view(), name='region-delete'),
]
