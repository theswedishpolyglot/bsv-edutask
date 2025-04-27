"""Tests todos endpoints."""

import pytest
import json

def test_create_and_get_todo(client):
    """Test creating and fetching a todo."""
    resp = client.post('/todos/create', data={'description': 'd', 'done': 'false'})
    assert resp.status_code == 200
    tid = resp.get_json()['_id']['$oid']
    resp2 = client.get(f'/todos/byid/{tid}')
    assert resp2.status_code == 200
    assert resp2.get_json()['description'] == 'd'

def test_create_todo_missing_description_returns_400(client):
    """Test creating a todo without description."""
    resp = client.post("/todos/create", data={'done': 'false'})
    assert resp.status_code == 400

def test_get_todo_malformed_id_400(client):
    """Test fetching a todo with a malformed ID."""
    resp = client.get("/todos/byid/not-an-oid")
    assert resp.status_code == 400

def test_update_todo(client):
    """Test updating a todo."""
    resp = client.post('/todos/create', data={'description': 'x', 'done': 'false'})
    tid = resp.get_json()['_id']['$oid']
    payload = json.dumps({'$set': {'done': True}})
    resp2 = client.put(f'/todos/byid/{tid}', data={'data': payload})
    assert resp2.status_code == 200
    assert client.get(f'/todos/byid/{tid}').get_json()['done'] is True

def test_delete_todo(client):
    """Test deleting a todo."""
    resp = client.post('/todos/create', data={'description': 'y', 'done': 'false'})
    tid = resp.get_json()['_id']['$oid']
    resp2 = client.delete(f'/todos/byid/{tid}')
    assert resp2.status_code == 200
    assert resp2.get_json()['id'] == tid
