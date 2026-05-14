import pytest


def test_root_redirect(client):
    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200  # RedirectResponse returns 200? Wait, no, RedirectResponse is 307 by default, but TestClient follows redirects?
    # Actually, TestClient follows redirects by default, so it will get the static file, but since it's mounted, it might not.
    # To test redirect, perhaps use follow_redirects=False
    # But for simplicity, since it's redirect to static, maybe skip or test differently.
    # Actually, let's test that it redirects.
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    # Arrange - No special setup needed for this endpoint

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # Based on the app's activities database

    # Check that each activity has the expected structure
    for activity_name, activity_data in data.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_signup_activity_full(client):
    # Arrange
    activity_name = "Chess Club"
    # Chess Club has max 12, starts with 2 participants
    # Sign up 10 more to reach max
    emails = [f"student{i}@example.com" for i in range(10)]
    for email in emails:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200

    # Now try to signup one more
    extra_email = "extra@example.com"
    response = client.post(f"/activities/{activity_name}/signup?email={extra_email}")

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Activity is full" in data["detail"]


def test_signup_successful(client):
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]

    # Verify the student was added to participants
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate@example.com"

    # First signup
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act - Try to signup again
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_invalid_activity(client):
    # Arrange
    invalid_activity = "NonExistent Activity"
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


def test_unregister_successful(client):
    # Arrange
    activity_name = "Programming Class"
    email = "unregister@example.com"

    # First signup
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]

    # Verify the student was removed from participants
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_participant_not_found(client):
    # Arrange
    activity_name = "Programming Class"
    email = "notsignedup@example.com"

    # Act - Try to unregister without signing up first
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Participant not found" in data["detail"]


def test_unregister_invalid_activity(client):
    # Arrange
    invalid_activity = "Invalid Activity"
    email = "student@example.com"

    # Act
    response = client.delete(f"/activities/{invalid_activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]