from urllib.parse import quote


def test_get_activities_returns_activities(client):
    # Arrange
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    path = f"/activities/{quote(activity)}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    assert email in client.get("/activities").json()[activity]["participants"]


def test_unregister_participant_removes_it(client):
    # Arrange
    activity = "Programming Class"
    email = "tempstudent@mergington.edu"
    signup_path = f"/activities/{quote(activity)}/signup"
    delete_path = f"/activities/{quote(activity)}/participants"

    signup_response = client.post(signup_path, params={"email": email})
    assert signup_response.status_code == 200

    # Act
    response = client.delete(delete_path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_delete_nonexistent_participant_returns_404(client):
    # Arrange
    activity = "Gym Class"
    email = "notregistered@mergington.edu"
    path = f"/activities/{quote(activity)}/participants"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_invalid_activity_returns_404(client):
    # Arrange
    activity = "Invalid Activity"
    email = "someone@mergington.edu"
    path = f"/activities/{quote(activity)}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
