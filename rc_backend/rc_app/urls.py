from django.urls import path

from .views import public
from .views.auth import LoginUser, LogoutUser, RegisterUser
from .views.competition_views import *
from .views.profile_views import ProfilesListView, ProfileDetailView, ProfileUpdateView, PendingTeamInvitationsListView, \
    MyProfileDetailView, AcceptInvitationView, DeclineInvitationView, DeclineJoinRequestView, AcceptJoinRequestView
from .views.public import PublicRegionsDetailView
from .views.team_views import *

app_name = "rc_app"
urlpatterns = [
    path("", public.index, name="index"),
    # path("competition/<uuid:pk>/", PublicCompetitionsDetailView.as_view(), name="public_competition_details"),
    path("region/<uuid:pk>/", PublicRegionsDetailView.as_view(), name="public_region_details"),

    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),

    path('onboarding/', public.onboarding, name='onboarding'),

    path("competitions/", CompetitionListView.as_view(), name="competitions"),
    path("competition/<uuid:pk>/", CompetitionDetailView.as_view(), name="competition_details"),
    path("competitions/<uuid:pk>/", CompetitionDetailView.as_view(), name="competition_details"),
    path("competitions/<uuid:competition_id>/teams", TeamsForCompetitionListView.as_view(),
         name="competition_teams_list"),
    path("competitions/<uuid:competition_id>/member_search", MemberSearchListView.as_view(), name="competition_ms"),

    path('apply_for_position/<uuid:search_id>/', ApplyForPositionView.as_view(), name='apply_for_position'),

    path("profile/", MyProfileDetailView.as_view(), name="profile"),
    path("profiles/", ProfilesListView.as_view(), name="profiles"),
    path("profile/my_invites/", PendingTeamInvitationsListView.as_view(), name="profile_my_invites"),
    path("profiles/<uuid:pk>/", ProfileDetailView.as_view(), name="profile_detail"),
    path("profiles/<uuid:pk>/edit/", ProfileUpdateView.as_view(), name="edit_profile"),

    path("myteams/", MyTeamsListView.as_view(), name="my_teams_list"),
    path("myteams/join_requests", LeaderPendingJoinRequestsListView.as_view(), name="my_join_requests"),

    path("team/<uuid:pk>/", TeamDetailsView.as_view(), name="team_details"),
    path("team/<uuid:pk>/edit", TeamUpdateView.as_view(), name="team_details_update"),
    path("team/<uuid:pk>/delete", TeamDeleteView.as_view(), name="team_details_delete"),
    path("competitions/<uuid:competition_id>/new_team", TeamCreateView.as_view(), name="team_details_new"),
    path("team/<uuid:team_id>/disband", DisbandTeamView.as_view(), name="team_disband"),
    path("team/<uuid:team_id>/leave", TeamLeaveView.as_view(), name="team_leave"),

    path("team/<uuid:pk>/request", MemberSearchDetailView.as_view(), name="member_search_details"),
    path("team/<uuid:pk>/request/edit", MemberSearchUpdateView.as_view(), name="member_search_edit"),
    path("team/<uuid:pk>/request/new", MemberSearchCreateView.as_view(), name="member_search_create"),
    # path("team/<uuid:pk>/join/all", LeaderPendingJoinRequestsListView.as_view(), name="leader_pending_join_requests"),
    path("team/<uuid:pk>/join/<uuid:pk2>", LeaderPendingJoinRequestUpdateView.as_view(),
         name="leader_pending_join_update"),

    path('accept_invitation/<uuid:invitation_id>/', AcceptInvitationView.as_view(), name='accept_invitation'),
    path('decline_invitation/<uuid:invitation_id>/', DeclineInvitationView.as_view(), name='decline_invitation'),

    path('accept_join_request/<uuid:request_id>/', AcceptJoinRequestView.as_view(), name='accept_join_request'),
    path('decline_join_request/<uuid:request_id>/', DeclineJoinRequestView.as_view(), name='decline_join_request'),

    # path("competitions/<uuid:competition_id>/member_searches/<uuid:team_id>/new",
    #      WannabePendingJoinRequestCreateView.as_view(),
    #      name="join_request_new"),
    # path("competitions/<uuid:competition_id>/member_searches/<uuid:team_id>/delete",
    #      WannabePendingJoinRequestDeleteView.as_view(), name="join_request_delete"),

]
