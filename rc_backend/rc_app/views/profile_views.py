from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView

from rc_backend.rc_app.models import Team, Competition, CompetitionResult, FSP
from rc_backend.rc_app.models.enums import TeamInvitationEnum
from rc_backend.rc_app.models.invitation import TeamInvitation
from rc_backend.rc_app.models.join_request import JoinRequest
from rc_backend.rc_app.models.profile import Profile


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
                'competition_id': str(result.team.competition),
                'team_id': str(result.team.id),
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
    template_name = 'rc_app/profile_detail.html'

    def get_object(self, queryset=None):
        # Return the profile of the currently logged-in user
        return self.request.user.profile


class ProfileDetailView(DetailView):
    model = Profile

    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        data = combine_profile_data(profile)
        context["data"] = data
        return context
        # return render(request, self.template_name, context)


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['name', 'last_name', 'email', 'description', 'fsp']
    success_url = reverse_lazy('rc_app:profile')

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

        # Ensure the current user is the invitee
        if invitation.invitee != request.user.profile:
            return HttpResponseForbidden("You are not authorized to accept this invitation.")

        # Update the invitation status and add the user to the team
        invitation.invitation_status = 'ACCEPTED'
        invitation.save()

        # Add the invitee to the team members
        invitation.inviter_team.team_members.add(invitation.invitee)

        return redirect('rc_app:profile_my_invites')


class DeclineInvitationView(LoginRequiredMixin, View):
    def post(self, request, invitation_id):
        invitation = get_object_or_404(TeamInvitation, id=invitation_id)

        # Ensure the current user is the invitee
        if invitation.invitee != request.user.profile:
            return HttpResponseForbidden("You are not authorized to decline this invitation.")

        # Update the invitation status
        invitation.invitation_status = 'DECLINED'
        invitation.save()

        return redirect('rc_app:profile_my_invites')


class AcceptJoinRequestView(LoginRequiredMixin, View):
    def post(self, request, request_id):
        join_request = get_object_or_404(JoinRequest, id=request_id)

        # Ensure the current user is the leader of the team
        if join_request.team.leader != request.user.profile:
            return HttpResponseForbidden("You are not authorized to accept this join request.")

        # Update the join request status and add the user to the team
        join_request.join_status = 'ACCEPTED'
        join_request.save()

        # Add the requester to the team members
        join_request.team.team_members.add(join_request.profile)

        return redirect('rc_app:leader_pending_join_update')


class DeclineJoinRequestView(LoginRequiredMixin, View):
    def post(self, request, request_id):
        join_request = get_object_or_404(JoinRequest, id=request_id)

        # Ensure the current user is the leader of the team
        if join_request.team.leader != request.user.profile:
            return HttpResponseForbidden("You are not authorized to decline this join request.")

        # Update the join request status
        join_request.join_status = 'DECLINED'
        join_request.save()

        return redirect('rc_app:leader_pending_join_update')
