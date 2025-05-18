from django.urls import path
from ..regions.regions_list import RegionListView
from ..regions.region_detail import RegionDetailView

app_name = 'regions'

urlpatterns = [
    path('', RegionListView.as_view(), name='list'),
    # path('create/', RegionCreateView.as_view(), name='create'),
    path('<int:id>/', RegionDetailView.as_view(), name='detail'),
    # path('<int:pk>/update/', RegionUpdateView.as_view(), name='update'),
    # path('<int:pk>/delete/', RegionDeleteView.as_view(), name='delete'),
]