from django.core.exceptions import PermissionDenied
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView, ListView

from src.core.models import Profile
from src.core.models.enums import JoinRequestEnum
from src.core.models.join_request import JoinRequest


class LeaderPendingJoinRequestsListView(ListView):
    """request that other people have sent to my team"""
    model = JoinRequest
    template_name = 'core/leader_join_requests_list.html'
    context_object_name = 'join_requests'

    def get_queryset(self):
        profile = self.request.user.profile

        return (JoinRequest.objects
                .filter(team__leader=profile)
                .filter(join_status=JoinRequestEnum.PENDING))


class LeaderPendingJoinRequestUpdateView(UpdateView):
    model = JoinRequest
    fields = ["status"]

    def dispatch(self, request, *args, **kwargs):
        join_request: JoinRequest = self.get_object()
        team = join_request.team
        profile = get_object_or_404(Profile, user=self.request.user)

        if team.leader != profile:
            raise PermissionDenied("You do not have permission to delete this team.")
        return super().dispatch(request, *args, **kwargs)
