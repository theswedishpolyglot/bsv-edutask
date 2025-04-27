"""Tests tasks endpoints."""

import pytest
import json

def test_get_task(client, task_id):
    """Test fetching a task by ID."""
    resp = client.get(f'/tasks/byid/{task_id}')
    assert resp.status_code == 200
    assert resp.get_json()['_id']['$oid'] == task_id

def test_get_task_malformed_id_400(client):
    """Test fetching a task with a malformed ID."""
    resp = client.get("/tasks/byid/not-an-oid")
    assert resp.status_code == 400

def test_create_task_success(client, user_id):
    """Test creating a task."""
    resp = client.post(
        '/tasks/create',
        data={
            'userid': user_id,
            'title': 'New Task',
            'description': 'Desc',
            'url': 'vid123',
            'todos': ['init']
        }
    )
    assert resp.status_code == 200
    tasks = resp.get_json()
    assert isinstance(tasks, list) and any(t['_id']['$oid'] for t in tasks)

@pytest.mark.parametrize('field', ['title', 'description', 'url'])
def test_create_task_missing_required_returns_400(client, user_id, field):
    """Test creating a task with missing required fields."""
    payload = {'userid': user_id, 'title': 'T', 'description': 'D', 'url': 'u', 'todos': ['init']}
    payload.pop(field)
    resp = client.post('/tasks/create', data=payload)
    assert resp.status_code == 400

def test_delete_task(client, task_id):
    """Test deleting a task."""
    resp = client.delete(f'/tasks/byid/{task_id}')
    assert resp.status_code == 200
    assert resp.get_json()['success']

def test_update_task_valid(client, task_id):
    """Test updating a task."""
    payload = json.dumps({'$set': {'title': 'Updated Title'}})
    resp = client.put(f'/tasks/byid/{task_id}', data={'data': payload})
    assert resp.status_code == 200
    assert resp.get_json()['title'] == 'Updated Title'
