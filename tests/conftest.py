import pytest
import copy
from fastapi.testclient import TestClient

from src.app import app, activities

# Initial state of activities
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice team drills and compete in school basketball games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu", "maria@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Develop soccer skills and enjoy friendly matches",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["kevin@mergington.edu", "nina@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore painting, drawing, and mixed media art projects",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["lily@mergington.edu", "josiah@mergington.edu"]
    },
    "Drama Club": {
        "description": "Practice acting, improv, and put on school performances",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["sarah@mergington.edu", "mason@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Prepare for science competitions and explore STEM challenges",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["oliver@mergington.edu", "zara@mergington.edu"]
    },
    "Debate Team": {
        "description": "Build public speaking and argumentation skills through debates",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["liam@mergington.edu", "emma@mergington.edu"]
    }
}


@pytest.fixture
def client():
    # Reset activities to initial state before each test
    activities.clear()
    activities.update(copy.deepcopy(initial_activities))
    return TestClient(app)