from rc_backend.rc_app.models import ModerationEnum


# Create your tests here.

# Successfully creates a team with valid name, competition_id, and leader_id
def test_create_team_with_valid_parameters(self, mocker):
    # Arrange
    mock_request = mocker.Mock()
    mock_request.method = "POST"
    mock_request.POST = {
        "name": "Test Team",
        "competition_id": "comp-123"
    }
    mock_request.user = mocker.Mock()
    mock_request.user.id = "user-123"

    mock_team_repo = mocker.patch('rc_backend.rc_app.views.team_views.TeamRepo')
    mock_uuid = mocker.patch('rc_backend.rc_app.views.team_views.uuid')
    mock_uuid.uuid4.return_value = "team-123"

    # Act
    from rc_backend.rc_app.views.team_views import create_team
    result = create_team(mock_request)

    # Assert
    mock_team_repo.create.assert_called_once_with(
        team_id="team-123",
        title="Test Team",
        competition_id="comp-123",
        leader_id="user-123",
        moderation_status=ModerationEnum.PENDING
    )
