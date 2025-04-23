from django.urls import path

from .views import public
from .views.auth import LoginUser, LogoutUser, RegisterUser
from .views.competition_views import *
from .views.profile_views import ProfilesListView, ProfileDetailView, EditProfileDetailView
from .views.public import PublicCompetitionsDetailView, PublicRegionsDetailView
from .views.team_views import *

app_name = "rc_app"
urlpatterns = [
    path("", public.index, name="index"),
    path("competition/<uuid:pk>/", PublicCompetitionsDetailView.as_view(), name="public_competition_details"),
    path("region/<uuid:pk>/", PublicRegionsDetailView.as_view(), name="public_region_details"),

    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),

    path("competitions/", CompetitionListView.as_view(), name="competitions"),
    path("competitions/<uuid:pk>/", CompetitionDetailView.as_view(), name="competition_details"),

    path("profiles/", ProfilesListView.as_view(), name="profiles"),
    path("profiles/<uuid:pk>/", ProfileDetailView.as_view(), name="profile_details"),
    path("profiles/<uuid:pk>/edit/", EditProfileDetailView.as_view(), name="edit_profile"),

    path("team/<uuid:pk>/", TeamDetailsView.as_view(), name="team_details"),
    path("team/<uuid:pk>/edit", TeamUpdateView.as_view(), name="team_details_update"),
    path("team/<uuid:pk>/delete", TeamDeleteView.as_view(), name="team_details_delete"),
    path("team/<uuid:pk>/new", TeamCreateView.as_view(), name="team_details_new"),

    path("team/<uuid:pk>/request", MemberSearchDetailView.as_view(), name="member_search_details"),
    path("team/<uuid:pk>/request/edit", MemberSearchUpdateView.as_view(), name="member_search_edit"),
    path("team/<uuid:pk>/request/new", MemberSearchCreateView.as_view(), name="member_search_create"),
    path("team/<uuid:pk>/join/all", LeaderPendingJoinRequestsListView.as_view(), name="leader_pending_join_requests"),
    path("team/<uuid:pk>/join/<uuid:pk2>", LeaderPendingJoinRequestUpdateView.as_view(),
         name="leader_pending_join_update"),

    path("competitions/<uuid:competition_id>/member_searches", MemberSearchListView.as_view(),
         name="member_searches"),
    path("competitions/<uuid:competition_id>/member_searches/<uuid:team_id>/new",
         WannabePendingJoinRequestCreateView.as_view(),
         name="join_request_new"),
    path("competitions/<uuid:competition_id>/member_searches/<uuid:team_id>/delete",
         WannabePendingJoinRequestDeleteView.as_view(), name="join_request_delete"),

]
