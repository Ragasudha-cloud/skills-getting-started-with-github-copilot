import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


# Store original activities state for resetting
ORIGINAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture
def client():
    """Fixture that provides a TestClient for making requests to the app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Fixture that resets the activities database to original state before each test"""
    # Arrange: Reset to original state
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield
    # Cleanup: Reset after test completes
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
