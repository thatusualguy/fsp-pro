from django.urls import path

from .views.auth.login import LoginUser
from .views.auth.logout import LogoutUser
from .views.auth.register import RegisterUser
from .views.profile.profile import MyProfileDetailView, ProfileDetailView, ProfileUpdateView
from .views.profile.profile_list import ProfilesListView
from .views.public import public
from src.core.views.competition.competition import *
from src.core.views.public.public import PublicRegionsDetailView
from .views.competition.teams_list import TeamsForCompetitionListView
from .views.team.invitation import PendingTeamInvitationsListView, AcceptInvitationView, DeclineInvitationView
from .views.team.join_request_views import ApplyForPositionView
from .views.team.leader_member_views import LeaderPendingJoinRequestsListView, LeaderPendingJoinRequestUpdateView
from .views.team.member_search_views import MemberSearchDetailView, MemberSearchUpdateView, MemberSearchCreateView
from .views.team.request import AcceptJoinRequestView, DeclineJoinRequestView
from .views.team.search import MemberSearchListView
from .views.team.team import TeamDeleteView, TeamDetailsView, MyTeamsListView
from .views.team.team_create import TeamCreateView
from .views.team.team_management_views import DisbandTeamView, TeamLeaveView
from .views.team.team_update import TeamUpdateView, send_team_to_moderation

app_name = "core"
urlpatterns = [
    # path("", public.index, name="index"),
    path("about", public.about, name="about"),
    path("regions", public.regions, name="regions"),
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
    path("competitions/<uuid:competition_id>/search", MemberSearchListView.as_view(), name="member_searches"),

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

    path('team/<uuid:team_id>/send_to_moderation/', send_team_to_moderation, name='send_team_to_moderation'),

    path("team/<uuid:pk>/request", MemberSearchDetailView.as_view(), name="member_search_details"),
    path("team/<uuid:pk>/request/edit", MemberSearchUpdateView.as_view(), name="member_search_edit"),
    path("team/<uuid:pk>/request/new", MemberSearchCreateView.as_view(), name="member_search_create"),
    path("team/<uuid:pk>/join/<uuid:pk2>", LeaderPendingJoinRequestUpdateView.as_view(),
         name="leader_pending_join_update"),

    path('accept_invitation/<uuid:invitation_id>/', AcceptInvitationView.as_view(), name='accept_invitation'),
    path('decline_invitation/<uuid:invitation_id>/', DeclineInvitationView.as_view(), name='decline_invitation'),

    path('accept_join_request/<uuid:request_id>/', AcceptJoinRequestView.as_view(), name='accept_join_request'),
    path('decline_join_request/<uuid:request_id>/', DeclineJoinRequestView.as_view(), name='decline_join_request'),
]
