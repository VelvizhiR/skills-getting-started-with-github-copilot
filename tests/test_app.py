from fastapi.testclient import TestClient

from src.app import app
from src import app as app_module


client = TestClient(app)


def test_signup_updates_activity_participants():
    app_module.activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    response = client.post(
        "/activities/Chess%20Club/signup?email=student@mergington.edu"
    )

    assert response.status_code == 200
    activities_response = client.get("/activities")
    chess_club = activities_response.json()["Chess Club"]
    assert "student@mergington.edu" in chess_club["participants"]


def test_unregister_participant_removes_email():
    app_module.activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    response = client.delete(
        "/activities/Chess%20Club/participants/michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "michael@mergington.edu" in response.json()["message"]

    activities_response = client.get("/activities")
    chess_club = activities_response.json()["Chess Club"]
    assert "michael@mergington.edu" not in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]
