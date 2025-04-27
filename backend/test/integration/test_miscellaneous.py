"""Miscellaneous integration tests."""

import pytest

def test_ping(client):
    """Test the ping endpoint."""
    resp = client.get('/')
    assert resp.status_code == 200
    body = resp.get_json()
    assert 'version' in body

def test_populate_returns_users(client):
    """Test the populate endpoint returns users."""
    resp = client.post('/populate')
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data.get('users'), list) and data['users']
