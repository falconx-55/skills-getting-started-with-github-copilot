from fastapi.testclient import TestClient
from src.app import app
import uuid

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    test_email = f"test-{uuid.uuid4().hex[:8]}@example.com"
    activity = "Chess Club"

    # Ensure not present before
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert test_email not in resp.json()[activity]["participants"]

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json()["message"]

    # Confirm present
    resp = client.get("/activities")
    assert test_email in resp.json()[activity]["participants"]

    # Unregister
    resp = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert resp.status_code == 200

    # Confirm removed
    resp = client.get("/activities")
    assert test_email not in resp.json()[activity]["participants"]
