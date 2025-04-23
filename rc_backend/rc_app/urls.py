from django.urls import path

from .views import public
from .views.competition_views import *

app_name = "rc_app"
urlpatterns = [
    path("", public.index, name="index"),

    path("competitions/", CompetitionListView.as_view(), name="competitions"),
    path("competitions/<uuid:pk>/", CompetitionDetailView.as_view(), name="competition_details"),

    # path("profiles/", ProfilesListView.as_view(), name="profiles"),
    # path("profiles/<uuid:pk>/", ProfileDetailView.as_view(), name="profile_details"),
    # path("profiles/<uuid:pk>/edit/", EditProfileDetailView.as_view(), name="edit_profile"),

]
