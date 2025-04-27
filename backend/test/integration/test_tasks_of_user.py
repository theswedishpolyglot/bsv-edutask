"""Test tasks of user endpoints."""

import pytest

def test_list_tasks_of_new_user_returns_empty(client, user_id):
    """Test that a new user has no tasks."""
    resp = client.get(f"/tasks/ofuser/{user_id}")
    assert resp.status_code == 200
    assert resp.get_json() == []

def test_list_tasks_of_unknown_user_returns_404(client):
    """Test that a non-existent user returns 404."""
    fake_id = "a" * 24
    resp = client.get(f"/tasks/ofuser/{fake_id}")
    assert resp.status_code == 404

def test_list_tasks_with_malformed_userid_400(client):
    """Test that a malformed user ID returns 400."""
    resp = client.get("/tasks/ofuser/not-an-oid")
    assert resp.status_code == 400

def test_list_tasks_of_user_with_tasks(client, user_id):
    """Test that a user with tasks returns the correct tasks."""
    resp = client.get(f"/tasks/ofuser/{user_id}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list) and len(data) > 0
