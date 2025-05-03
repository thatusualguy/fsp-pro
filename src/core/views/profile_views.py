from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView

from src.core.models import Team, Competition, CompetitionResult, FSP
from src.core.models.enums import TeamInvitationEnum
from src.core.models.invitation import TeamInvitation
from src.core.models.join_request import JoinRequest
from src.core.models.profile import Profile


class ProfilesListView(ListView):
    model = Profile
    paginate_by = 50


def combine_profile_data(profile):
    teams_as_leader = Team.objects.filter(leader_id=profile.id)
    teams_as_member = Team.objects.filter(team_members__id=profile.id)

    # Combine the teams
    all_teams = teams_as_leader | teams_as_member

    # Get all competitions the profile has participated in
    competitions = Competition.objects.filter(team__in=all_teams).distinct()

    # Get all competition results for these teams
    competition_results = CompetitionResult.objects.filter(team__in=all_teams).distinct()

    print(competition_results)
    # Prepare the response data
    data = {
        'teams': all_teams,
        'competitions': competitions,
        'competition_results': [
            {
                'result_id': str(result.id),
                'competition_id': str(result.team.competition.id),
                'competition_name': str(result.team.competition.title),
                'team_id': str(result.team.id),
                'team_title': str(result.team.title),
                'points': result.points,
                'place': result.place
            } for result in competition_results if result is not None
        ]
    }
    pprint(data)
    return data


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['name', 'last_name', 'email', 'description']
#

class MyProfileDetailView(DetailView):
    model = Profile
    template_name = 'core/profile_detail.html'

    def get_object(self, queryset=None):
        # Return the profile of the currently logged-in user
        return self.request.user.profile

    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        data = combine_profile_data(profile)
        context["data"] = data
        pprint(context)
        return context


class ProfileDetailView(DetailView):
    model = Profile

    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        data = combine_profile_data(profile)
        context["data"] = data
        pprint(context)
        return context
        # return render(request, self.template_name, context)


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['name', 'last_name', 'email', 'description', 'fsp']
    success_url = reverse_lazy('core:profile')

    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context["fsps"] = FSP.objects.all()

        return context


# user invited to team


class PendingTeamInvitationsListView(ListView, LoginRequiredMixin):
    model = TeamInvitation

    def get_queryset(self):
        profile = self.request.user.profile
        # Filter invitations where the invitee is the current user

        data = (TeamInvitation.objects
                .filter(invitation_status=TeamInvitationEnum.PENDING)
                .filter(invitee=profile))
        pprint(data)
        return data


class AcceptInvitationView(LoginRequiredMixin, View):
    def post(self, request, invitation_id):
        invitation = get_object_or_404(TeamInvitation, id=invitation_id)

        # Check team size limit before accepting the invitation
        team = invitation.inviter_team
        competition = team.competition
        current_team_size = team.team_members.count() + 1  # +1 for leader
        max_team_size = competition.max_participants

        if current_team_size >= max_team_size:
            return HttpResponseForbidden("Cannot accept invitation. Team size limit reached.")

        # Ensure the current user is the invitee
        if invitation.invitee != request.user.profile:
            return HttpResponseForbidden("You are not authorized to accept this invitation.")

        # Ensure the invitee is from the same FSP as the leader
        if invitation.invitee.fsp != invitation.inviter_team.leader.fsp:
            return HttpResponseForbidden("Invitee must be from the same FSP as the team leader.")

        # Update the invitation status and add the user to the team
        invitation.invitation_status = 'ACCEPTED'
        invitation.save()

        # Add the invitee to the team members
        invitation.inviter_team.team_members.add(invitation.invitee)

        return redirect('core:profile_my_invites')


class DeclineInvitationView(LoginRequiredMixin, View):
    def post(self, request, invitation_id):
        invitation = get_object_or_404(TeamInvitation, id=invitation_id)

        # Ensure the current user is the invitee
        if invitation.invitee != request.user.profile:
            return HttpResponseForbidden("You are not authorized to decline this invitation.")

        # Update the invitation status
        invitation.invitation_status = 'DECLINED'
        invitation.save()

        return redirect('core:profile_my_invites')


class AcceptJoinRequestView(LoginRequiredMixin, View):
    def post(self, request, request_id):
        join_request = get_object_or_404(JoinRequest, id=request_id)

        # Check team size limit before accepting the join request
        team = join_request.team
        competition = team.competition
        current_team_size = team.team_members.count() + 1  # +1 for leader
        max_team_size = competition.max_participants

        if current_team_size >= max_team_size:
            return HttpResponseForbidden("Cannot accept join request. Team size limit reached.")

        # Ensure the current user is the leader of the team
        if join_request.team.leader != request.user.profile:
            return HttpResponseForbidden("You are not authorized to accept this join request.")

        # Ensure the invitee is from the same FSP as the leader
        if join_request.profile.fsp != join_request.team.leader.fsp:
            return HttpResponseForbidden("Must be from the same FSP as the team leader.")

        # Update the join request status and add the user to the team
        join_request.join_status = 'ACCEPTED'
        join_request.save()

        # Add the requester to the team members
        join_request.team.team_members.add(join_request.profile)

        return redirect('core:leader_pending_join_update')


class DeclineJoinRequestView(LoginRequiredMixin, View):
    def post(self, request, request_id):
        join_request = get_object_or_404(JoinRequest, id=request_id)

        # Ensure the current user is the leader of the team
        if join_request.team.leader != request.user.profile:
            return HttpResponseForbidden("You are not authorized to decline this join request.")

        # Update the join request status
        join_request.join_status = 'DECLINED'
        join_request.save()

        return redirect('core:leader_pending_join_update')
