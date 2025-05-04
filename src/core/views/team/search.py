from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from src.core.models import Competition
from src.core.models.enums import JoinRequestEnum
from src.core.models.join_request import JoinRequest
from src.core.models.team import MemberSearch
from src.core.views.team.helpers import already_in_team_for_competition


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
