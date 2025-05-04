from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView

from src.core.models import Team, Profile
from src.core.models.team import MemberSearch


class MemberSearchCreateView(CreateView):
    model = MemberSearch
    fields = "__all__"

    def dispatch(self, request, *args, **kwargs):
        ms: MemberSearch = self.get_object()
        team: Team = ms.team
        profile = get_object_or_404(Profile, user=self.request.user)

        if team.leader != profile:
            raise PermissionDenied("You do not have permission to create member search.")

        if team.competition.max_participants == 1:
            raise PermissionDenied("Cannot create member searches for competitions with max team size of 1.")

        return super().dispatch(request, *args, **kwargs)


class MemberSearchUpdateView(UpdateView):
    model = MemberSearch
    fields = "__all__"

    def dispatch(self, request, *args, **kwargs):
        ms: MemberSearch = self.get_object()
        profile = get_object_or_404(Profile, user=self.request.user)
        team = ms.team

        if team.leader != profile:
            raise PermissionDenied("You do not have permission to delete this team.")

        return super().dispatch(request, *args, **kwargs)


class MemberSearchDetailView(DetailView):
    model = MemberSearch
    fields = "__all__"
