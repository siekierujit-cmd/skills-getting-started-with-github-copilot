import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_unregister_participant_removes_their_email(client):
    original_activities = copy.deepcopy(activities)
    try:
        activity_name = "Chess Club"
        email = "new.student@mergington.edu"

        signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert signup_response.status_code == 200
        assert email in activities[activity_name]["participants"]

        unregister_response = client.delete(f"/activities/{activity_name}/signup?email={email}")
        assert unregister_response.status_code == 200
        assert email not in activities[activity_name]["participants"]
    finally:
        activities.clear()
        activities.update(original_activities)
