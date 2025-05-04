from django import forms
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, FormView

from src.core.models import Team, Profile
from src.core.models.join_request import JoinRequest
from src.core.models.team import MemberSearch
from src.core.views.team.helpers import already_in_team_for_competition


class JoinRequestForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea, label="Description", required=False)


class ApplyForPositionView(LoginRequiredMixin, FormView):
    form_class = JoinRequestForm
    template_name = 'core/joinrequest_form.html'

    def get_success_url(self):
        search_id = self.kwargs['search_id']
        member_search = get_object_or_404(MemberSearch, id=search_id)
        competition_id = member_search.team.competition.id
        return reverse_lazy('core:competition_ms', kwargs={'competition_id': competition_id})

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

        if already_in_team_for_competition(member_search.team.competition, self.request.user.profile):
            return HttpResponseForbidden("You are already a member of the team.")

        JoinRequest.objects.create(
            profile=self.request.user.profile,
            team=member_search.team,
            description=form.cleaned_data['description'],
            join_status='PENDING'
        )

        return super().form_valid(form)


class WannabePendingJoinRequestsListView(ListView):
    """request that i sent to other teams"""
    model = JoinRequest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
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

        if leader.fsp != profile.fsp:
            raise PermissionDenied("You do not have permission to join this team.")
        return super().dispatch(request, *args, **kwargs)


class WannabePendingJoinRequestDeleteView(DeleteView):
    model = JoinRequest

    def dispatch(self, request, *args, **kwargs):
        join_request: JoinRequest = self.get_object()
        profile = get_object_or_404(Profile, user=self.request.user)

        if profile != join_request.profile:
            raise PermissionDenied("You do not have permission to delete this join request.")
        return super().dispatch(request, *args, **kwargs)
