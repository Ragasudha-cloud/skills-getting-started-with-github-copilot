import pytest
from src.app import activities


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities(self, client, reset_activities):
        """Test that GET /activities returns all activities"""
        # ARRANGE
        # (activities are already populated by reset_activities fixture)

        # ACT
        response = client.get("/activities")

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
        assert data["Chess Club"]["max_participants"] == 12
        assert len(data["Chess Club"]["participants"]) == 2


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client, reset_activities):
        """Test successful signup of a new participant"""
        # ARRANGE
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])

        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity_name}"
        assert email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count + 1

    def test_signup_activity_not_found(self, client, reset_activities):
        """Test signup fails when activity does not exist"""
        # ARRANGE
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_signup_duplicate_email(self, client, reset_activities):
        """Test signup fails when student is already registered"""
        # ARRANGE
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        initial_count = len(activities[activity_name]["participants"])

        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student already signed up for this activity"
        assert len(activities[activity_name]["participants"]) == initial_count


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success(self, client, reset_activities):
        """Test successful unregistration of a participant"""
        # ARRANGE
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Exists in Chess Club
        initial_count = len(activities[activity_name]["participants"])

        # ACT
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Unregistered {email} from {activity_name}"
        assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_activity_not_found(self, client, reset_activities):
        """Test unregister fails when activity does not exist"""
        # ARRANGE
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # ACT
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_unregister_not_registered(self, client, reset_activities):
        """Test unregister fails when student is not registered"""
        # ARRANGE
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"  # Not in Chess Club
        initial_count = len(activities[activity_name]["participants"])

        # ACT
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student not registered for this activity"
        assert len(activities[activity_name]["participants"]) == initial_count
