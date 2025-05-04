from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from src.core.models.join_request import JoinRequest


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
