from django.urls import path
from src.core.views.info import RegionView


app_name = "core"
urlpatterns = [
    path("info/", RegionView.as_view())
]
