from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rc_backend.rc_app.models.profile import Profile
from rc_backend.rc_app.models.team import TeamMember, CompetitionResult
from rc_backend.rc_app.views.utils import force_get, force_post


@force_get
def show_profile(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id)

    # Retrieve all team memberships for the profile
    team_memberships = TeamMember.objects.filter(profile_id=profile)

    # Construct the response data
    teams_data = []
    for membership in team_memberships:
        team = membership.team_id
        competition_result = CompetitionResult.objects.filter(team=team).first()

        if competition_result:
            competition = competition_result.competition_id
            position = competition_result.place
        else:
            competition = None
            position = None

        teams_data.append({
            "team_id": team.team_id,
            "team_title": team.title,
            "competition_name": competition.name if competition else "N/A",
            "position": position if position is not None else "N/A"
        })

    profile_data = {
        "profile_id": profile.profile_id,
        "name": profile.name,
        "email": profile.email,
        "teams": teams_data
    }

    return JsonResponse(profile_data)


@force_post
def edit_profile():
    pass
