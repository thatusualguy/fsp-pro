from django import forms
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from src.core.models import Team, Profile, Competition
from src.core.models.enums import CompetitionTypeEnum


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
        user: Profile = kwargs.pop('user', None)
        is_create = kwargs.pop('is_create', False)
        competition: Competition = kwargs.pop('competition', None)
        super().__init__(*args, **kwargs)

        # Условия для создания/обновления команды по уровню соревнования
        if competition:
            regions = competition.fsps.values_list('region', flat=True)
            match competition.competition_type:
                case CompetitionTypeEnum.FEDERAL:
                    raise PermissionDenied
                case CompetitionTypeEnum.REGIONAL:
                    if user.fsp.region not in regions:
                        raise PermissionDenied

        # Только лидер может обновлять/создавать свою команду
        if user != leader:
            raise PermissionDenied("Только лидер может создавать или редактировать свою команду.")

        if not is_create:
            # Если идёт редактирование, делаем поле названия только для чтения (например, нельзя менять)
            self.fields['title'].disabled = True

        if competition and competition.max_participants == 1:
            # Disable invitees field for single-member competitions
            self.fields['invitees'].disabled = True

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
    template_name = 'core/team_form.html'
    form_class = TeamCreateForm
    success_url = reverse_lazy('core:my_teams_list')

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
        return reverse('core:my_teams_list')
