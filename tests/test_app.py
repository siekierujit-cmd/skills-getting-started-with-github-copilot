import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_unregister_participant_removes_their_email(client):
    # Arrange
    original_activities = copy.deepcopy(activities)
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    try:
        # Act
        signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert signup
        assert signup_response.status_code == 200

        activities_response = client.get("/activities")
        assert activities_response.status_code == 200

        signed_up_participants = activities_response.json()[activity_name]["participants"]
        assert email in signed_up_participants

        # Act
        unregister_response = client.delete(f"/activities/{activity_name}/signup?email={email}")

        # Assert removal
        assert unregister_response.status_code == 200

        refreshed_response = client.get("/activities")
        assert refreshed_response.status_code == 200

        refreshed_participants = refreshed_response.json()[activity_name]["participants"]
        assert email not in refreshed_participants
    finally:
        activities.clear()
        activities.update(original_activities)
