from src.core.models import Team


def already_in_team_for_competition(competition, profile):
    is_in_team = (Team.objects.filter(competition=competition,
                                      team_members=profile) | Team.objects.filter(leader=profile, )
                  ).exists()
    return is_in_team
