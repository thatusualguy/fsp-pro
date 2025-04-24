from annoying.functions import get_object_or_None
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView, FormView

from rc_backend.rc_app.models import Team, Profile, Competition
from rc_backend.rc_app.models.invitation import TeamInvitation
from rc_backend.rc_app.models.join_request import JoinRequest
from rc_backend.rc_app.models.team import MemberSearch, CompetitionResult


##  TEAM
class TeamDetailsView(DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()

        members = team.team_members.all()
        leader = team.leader
        leader_fsp = leader.fsp
        competition = team.competition
        competition_result = get_object_or_None(CompetitionResult, team=team)

        context['members'] = members
        context['leader'] = leader
        context['competition'] = competition
        context['region'] = leader_fsp
        context['competition_result'] = competition_result
        return context


class TeamCreateForm(forms.ModelForm):
    invitees = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Invite Members"
    )

    class Meta:
        model = Team
        # fields = ['title', ]
        fields = ['title', 'invitees']

    def __init__(self, *args, **kwargs):
        leader = kwargs.pop('leader', None)
        user = kwargs.pop('user', None)
        competition = kwargs.pop('competition', None)
        super().__init__(*args, **kwargs)

        if user != leader:
            raise PermissionDenied

        if self.instance and self.instance.pk:
            # If the form is being used to edit an existing team, make the title field read-only
            self.fields['title'].disabled = True

        if leader:
            # Filter invitees to only include profiles from the same region as the leader
            self.fields['invitees'].queryset = Profile.objects.filter(fsp=leader.fsp).filter(~Q(id=leader.id))
        else:
            raise PermissionDenied

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Team.objects.filter(title=title).exists():
            raise ValidationError("A team with this title already exists.")
        return title


class TeamCreateView(LoginRequiredMixin, FormView):
    template_name = 'rc_app/team_form.html'
    form_class = TeamCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the leader to the form
        competition_id = self.kwargs.get('competition_id')
        kwargs['leader'] = self.request.user.profile
        kwargs['user'] = self.request.user.profile
        kwargs['competition'] = get_object_or_404(Competition, id=competition_id)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        competition_id = self.kwargs.get('competition_id')
        context['competition'] = get_object_or_404(Competition, id=competition_id)
        return context

    def form_valid(self, form):
        competition_id = self.kwargs['competition_id']
        competition = Competition.objects.get(id=competition_id)

        # Set the competition for the team
        form.instance.competition = competition

        # Set the current user as the team leader
        form.instance.leader = self.request.user.profile

        # Save the team
        response = super().form_valid(form)

        form.instance.team_members.add(self.request.user.profile)

        # Handle invitations
        invitees = form.cleaned_data['invitees']
        for invitee in invitees:
            TeamInvitation.objects.create(inviter_team=form.instance, invitee=invitee)

        return response

    def get_success_url(self):
        return reverse('rc_app:team_details', kwargs={'pk': self.object.pk})


class TeamUpdateView(UpdateView):
    model = Team
    fields = "__all__"

    def dispatch(self, request, *args, **kwargs):
        team: Team = self.get_object()
        # Get current user's profile
        profile = get_object_or_404(Profile, user=self.request.user)

        # Check if current user is the team leader
        if team.leader != profile:
            raise PermissionDenied("You do not have permission to update this team.")

        return super().dispatch(request, *args, **kwargs)


class MyTeamsListView(ListView):
    model = Team
    template_name = "rc_app/team_list.html"

    def get_queryset(self):
        member_teams = self.request.user.profile.member_teams.all()
        leader_teams = self.request.user.profile.leader_teams.all()
        return member_teams | leader_teams


class TeamDeleteView(DeleteView):
    model = Team

    def dispatch(self, request, *args, **kwargs):
        team: Team = self.get_object()
        # Get current user's profile
        profile = get_object_or_404(Profile, user=request.user)
        # Check if current user is the team leader
        if team.leader != profile:
            raise PermissionDenied("You do not have permission to delete this team.")
        return super().dispatch(request, *args, **kwargs)


## MEMBER SEARCH

class MemberSearchListView(ListView):
    model = MemberSearch
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        competition_id = self.kwargs['competition_id']
        competition = get_object_or_404(Competition, pk=competition_id)
        ms = MemberSearch.objects.filter(team__competition=competition)
        context['member_search'] = ms
        return context


class MemberSearchCreateView(CreateView):
    model = MemberSearch
    fields = "__all__"

    def dispatch(self, request, *args, **kwargs):
        ms: MemberSearch = self.get_object()
        # Get current user's profile
        profile = get_object_or_404(Profile, user=self.request.user)
        team: Team = ms.team

        # Check if current user is the team leader
        if team.leader != profile:
            raise PermissionDenied("You do not have permission to create member search.")
        return super().dispatch(request, *args, **kwargs)


class MemberSearchUpdateView(UpdateView):
    model = MemberSearch
    fields = "__all__"

    def dispatch(self, request, *args, **kwargs):
        ms: MemberSearch = self.get_object()
        # Get current user's profile
        profile = get_object_or_404(Profile, user=self.request.user)
        team = ms.team

        # Check if current user is the team leader
        if team.leader != profile:
            raise PermissionDenied("You do not have permission to delete this team.")
        return super().dispatch(request, *args, **kwargs)


class MemberSearchDetailView(DetailView):
    model = MemberSearch
    fields = "__all__"


# user invited to team
class PendingTeamInvitationsListView(ListView):
    model = TeamInvitation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get Profile of the current user
        profile = Profile.objects.get(user=self.request.user)
        # Get TeamInvitations where the current user is invited
        invitations = TeamInvitation.objects.filter(invitee=profile)

        context['invitations'] = invitations
        return context


# user asks to join team

# WANNABE SIDE
class WannabePendingJoinRequestsListView(ListView):
    """request that i sent to other teams"""
    model = JoinRequest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get Profile of the current user
        profile = Profile.objects.get(user=self.request.user)
        # Get TeamInvitations where the current user is invited
        invitations = JoinRequest.objects.filter(invitee=profile)

        context['invitations'] = invitations
        return context


class WannabePendingJoinRequestCreateView(CreateView):
    model = JoinRequest

    def dispatch(self, request, *args, **kwargs):
        join_request: JoinRequest = self.get_object()
        profile = get_object_or_404(Profile, user=self.request.user)
        team: Team = join_request.team
        leader: Profile = team.leader

        # Check if current user is the team leader
        if leader.fsp != profile.fsp:
            raise PermissionDenied("You do not have permission to join this team.")
        return super().dispatch(request, *args, **kwargs)


class WannabePendingJoinRequestDeleteView(DeleteView):
    model = JoinRequest

    def dispatch(self, request, *args, **kwargs):
        join_request: JoinRequest = self.get_object()
        profile = get_object_or_404(Profile, user=self.request.user)

        # Check if current user is the team leader
        if profile != join_request.profile:
            raise PermissionDenied("You do not have permission to delete this join request.")
        return super().dispatch(request, *args, **kwargs)


# LEADER SIDE


class LeaderPendingJoinRequestsListView(ListView):
    """request that other people have sent to my team"""
    model = JoinRequest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_id = kwargs.get("team_id")
        team = Team.objects.get(id=team_id)
        requests = JoinRequest.objects.filter(
            team=team
        )
        context['join_requests'] = requests
        return context


class LeaderPendingJoinRequestUpdateView(UpdateView):
    model = JoinRequest
    fields = ["status"]

    def dispatch(self, request, *args, **kwargs):
        join_request: JoinRequest = self.get_object()
        team = join_request.team
        profile = get_object_or_404(Profile, user=self.request.user)

        # Check if current user is the team leader
        if team.leader != profile:
            raise PermissionDenied("You do not have permission to delete this team.")
        return super().dispatch(request, *args, **kwargs)
