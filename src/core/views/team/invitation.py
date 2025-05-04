from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from src.core.models.enums import TeamInvitationEnum
from src.core.models.invitation import TeamInvitation


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
