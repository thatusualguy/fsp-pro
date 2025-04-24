from annoying.functions import get_object_or_None
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView, FormView

from rc_backend.rc_app.models import Team, Profile, Competition
from rc_backend.rc_app.models.enums import JoinRequestEnum, CompetitionTypeEnum
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
        context['now'] = timezone.now()
        context['competition'] = competition
        context['is_member'] = self.request.user.profile in team.team_members.all()
        context['region'] = leader_fsp
        context['competition_result'] = competition_result
        return context


class TeamCreateForm(forms.ModelForm):
    """
    Форма для создания и обновления команды.
    """
    invitees = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Пригласить участников"
    )

    class Meta:
        model = Team
        fields = ['title', 'invitees', ]

    def __init__(self, *args, **kwargs):
        """
        Дополнительные параметры:
          - leader: Profile (инициатор – будущий капитан)
          - user: Profile (текущий пользователь)
          - is_create: bool (True для создания, False для редактирования)
          - competition: Competition (соревнование, к которому относится команда)
        """
        leader = kwargs.pop('leader', None)
        user = kwargs.pop('user', None)
        is_create = kwargs.pop('is_create', False)
        competition: Competition = kwargs.pop('competition', None)
        super().__init__(*args, **kwargs)

        # Условия для создания/обновления команды по уровню соревнования
        if competition:
            if competition.competition_type == CompetitionTypeEnum.FEDERAL:
                raise PermissionDenied("Создание и изменение команды для федерального соревнования запрещено.")

        # Только лидер может обновлять/создавать свою команду
        if user != leader:
            raise PermissionDenied("Только лидер может создавать или редактировать свою команду.")

        if not is_create:
            # Если идёт редактирование, делаем поле названия только для чтения (например, нельзя менять)
            self.fields['title'].disabled = True

        # Ограничить доступные для приглашения пользователей одной областью (FSP)
        if leader:
            self.fields['invitees'].queryset = Profile.objects.filter(fsp=leader.fsp).exclude(id=leader.id)
        else:
            raise PermissionDenied("Не определён лидер команды.")

    def clean_title(self):
        """
        При обновлении пропускаем проверку уникальности — поле недоступно.
        При создании обязательно проверяем, что такого названия ещё нет.
        """
        title = self.cleaned_data.get('title')
        # Если поле отключено (редактирование) — не валидируем дубликаты
        if self.fields['title'].disabled:
            return title
        if Team.objects.filter(title=title).exists():
            raise ValidationError("Команда с таким названием уже существует.")
        return title


class TeamCreateView(LoginRequiredMixin, FormView):
    template_name = 'rc_app/team_form.html'
    form_class = TeamCreateForm
    success_url = reverse_lazy('rc_app:my_teams_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the leader to the form
        competition_id = self.kwargs.get('competition_id')
        kwargs['leader'] = self.request.user.profile
        kwargs['user'] = self.request.user.profile
        kwargs['is_create'] = True
        kwargs['competition'] = get_object_or_404(Competition, id=competition_id)

        if kwargs['competition'].competition_type == CompetitionTypeEnum.FEDERAL:
            raise PermissionDenied

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
        team = form.save()
        form.instance.team_members.add(self.request.user.profile)
        # TeamInvitation.objects.create(inviter_team=team)

        # Handle invitations
        invitees = form.cleaned_data['invitees']
        for invitee in invitees:
            form.instance.team_invitations.create(invitee=invitee)
            # TeamInvitation.objects.create(inviter_team=form.instance, invitee=invitee)

        # Team.objects.create(team)
        return redirect(self.success_url)

    def get_success_url(self):
        return reverse('rc_app:my_teams_list')


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
    context_object_name = 'member_searches'

    def get_queryset(self):
        competition_id = self.kwargs.get('competition_id')
        competition = get_object_or_404(Competition, pk=competition_id)
        return MemberSearch.objects.filter(team__competition=competition)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        competition_id = self.kwargs.get('competition_id')
        competition = get_object_or_404(Competition, pk=competition_id)
        user_profile = self.request.user.profile

        # Check if the user is already in a team for this competition
        is_in_team = already_in_team_for_competition(competition, user_profile)

        # Add a flag to each member search to indicate if the user has already applied
        member_searches = context['member_searches']
        for member_search in member_searches:
            member_search.has_applied = JoinRequest.objects.filter(
                profile=user_profile,
                team=member_search.team,
                join_status=JoinRequestEnum.PENDING
            ).exists()

        context['competition'] = competition
        context['is_in_team'] = is_in_team
        return context


class JoinRequestForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea, label="Description", required=False)


def already_in_team_for_competition(competition, profile):
    is_in_team = (Team.objects.filter(competition=competition,
                                      team_members=profile) | Team.objects.filter(leader=profile, )
                  ).exists()
    return is_in_team


class ApplyForPositionView(LoginRequiredMixin, FormView):
    form_class = JoinRequestForm
    template_name = 'rc_app/joinrequest_form.html'

    def get_success_url(self):
        search_id = self.kwargs['search_id']
        member_search = get_object_or_404(MemberSearch, id=search_id)
        competition_id = member_search.team.competition.id
        return reverse_lazy('rc_app:competition_ms', kwargs={'competition_id': competition_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_id = self.kwargs['search_id']
        member_search = get_object_or_404(MemberSearch, id=search_id)
        context['competition_name'] = member_search.team.competition.title
        context['team_name'] = member_search.team.title
        return context

    def form_valid(self, form):
        search_id = self.kwargs['search_id']
        member_search = get_object_or_404(MemberSearch, id=search_id)

        # Check if the user is already a member of the team
        if already_in_team_for_competition(member_search.team.competition, self.request.user.profile):
            return HttpResponseForbidden("You are already a member of the team.")

        # Process the application (e.g., create a join request)
        JoinRequest.objects.create(
            profile=self.request.user.profile,
            team=member_search.team,
            description=form.cleaned_data['description'],
            join_status='PENDING'
        )

        return super().form_valid(form)


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


class TeamLeaveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        team_id = kwargs.get('team_id')
        profile = request.user.profile
        team = get_object_or_404(Team, id=team_id)

        # Check if the user is the leader
        if team.leader == profile:
            raise PermissionDenied("The leader cannot leave the team. Please assign a new leader before leaving.")

        if team.competition.registration_until < timezone.now():
            raise PermissionDenied("You cannot leave after registration end.")

        # Check if the user is a member of the team
        if profile in team.team_members.all():
            team.team_members.remove(profile)
        else:
            raise PermissionDenied("You are not a member of this team.")

        return HttpResponseRedirect(reverse('rc_app:my_teams_list'))


class DisbandTeamView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        team = Team.objects.get(id=kwargs['team_id'])
        profile = request.user.profile

        print(kwargs['team_id'])
        # Check if the current user is the team leader
        if team.leader != profile:
            raise PermissionDenied("You do not have permission to disband this team.")

        if team.competition.registration_until > timezone.now():
            raise PermissionDenied("Too late.")

        # Disband the team
        team.disband()
        return redirect('rc_app:my_teams_list')


class MemberSearchDetailView(DetailView):
    model = MemberSearch
    fields = "__all__"


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
    template_name = 'rc_app/leader_join_requests_list.html'
    context_object_name = 'join_requests'

    def get_queryset(self):
        # Get the current user's profile
        profile = self.request.user.profile

        # Filter join requests for teams where the current user is the leader
        return (JoinRequest.objects
                .filter(team__leader=profile)
                .filter(join_status=JoinRequestEnum.PENDING))

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     team_id = kwargs.get("team_id")
    #     team = Team.objects.get(id=team_id)
    #     requests = JoinRequest.objects.filter(
    #         team=team
    #     )
    #     context['join_requests'] = requests
    #     return context


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
