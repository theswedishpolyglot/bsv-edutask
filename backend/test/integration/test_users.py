"""Tests users endpoints."""

import pytest

def test_list_users(client, user_id):
    """Test listing all users."""
    resp = client.get('/users/all')
    assert resp.status_code == 200
    ids = [u['_id']['$oid'] for u in resp.get_json()]
    assert user_id in ids

def test_get_user_by_id(client, user_id):
    """Test fetching a user by ID."""
    resp = client.get(f'/users/{user_id}')
    assert resp.status_code == 200
    assert resp.get_json()['_id']['$oid'] == user_id

def test_get_user_malformed_id_400(client):
    """Test fetching a user with a malformed ID."""
    resp = client.get("/users/not-an-oid")
    assert resp.status_code == 400

def test_get_user_by_email(client):
    """Test fetching a user by email."""
    email = 'test@example.com'
    resp = client.get(f'/users/bymail/{email}')
    assert resp.status_code == 200
    assert resp.get_json()['email'] == email

def test_get_user_by_email_invalid_format_400(client):
    """Test fetching a user by email with invalid format."""
    resp = client.get("/users/bymail/not-an-email")
    assert resp.status_code == 400

def test_update_user(client, user_id):
    """Test updating a user."""
    resp = client.put(f'/users/{user_id}', data={'firstName': 'Foo'})
    assert resp.status_code == 200
    assert resp.get_json()['firstName'] == 'Foo'

def test_update_user_malformed_id_400(client):
    """Test updating a user with a malformed ID."""
    resp = client.put("/users/not-an-oid", data={'firstName': 'X'})
    assert resp.status_code == 400

def test_delete_user(client, user_id):
    """Test deleting a user."""
    resp = client.delete(f'/users/{user_id}')
    assert resp.status_code == 200
    assert resp.get_json().get('success') is True

def test_create_user_success(client):
    """Test creating a user."""
    resp = client.post(
        '/users/create',
        data={'firstName': 'Test', 'lastName': 'Person', 'email': 'test@example.com'}
    )
    assert resp.status_code == 200
    user = resp.get_json()
    assert user['firstName'] == 'Test'
    assert user['lastName'] == 'Person'
    assert user['email'] == 'test@example.com'

@pytest.mark.parametrize('field', ['firstName', 'lastName', 'email'])
def test_create_user_missing_required_returns_400(client, field):
    """Test creating a user with missing required fields."""
    payload = {'firstName': 'A', 'lastName': 'B', 'email': 'a@b.com'}
    payload.pop(field)
    resp = client.post('/users/create', data=payload)
    assert resp.status_code == 400

def test_create_user_duplicate_email_returns_400(client):
    """Test creating a user with a duplicate email."""
    email = 'dup@example.com'
    assert client.post('/users/create', data={'firstName': 'X', 'lastName': 'Y', 'email': email}).status_code == 200
    resp = client.post('/users/create', data={'firstName': 'X2', 'lastName': 'Y2', 'email': email})
    assert resp.status_code == 400
