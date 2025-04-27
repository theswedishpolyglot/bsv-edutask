import mongomock
import pymongo

pymongo.MongoClient = mongomock.MongoClient

# Disable the validator option in mongomock
import mongomock.database as mdb
_orig_create = mdb.Database.create_collection

def _create_no_validator(self, name, **kwargs):
    """Create a collection without a validator in mongomock."""
    return _orig_create(self, name)
mdb.Database.create_collection = _create_no_validator

import pytest
import src.util.daos as daos_module
from main import app as flask_app

@pytest.fixture(autouse=True)
def clear_daos():
    """Clear DAO cache before and after each test to ensure isolation."""
    daos_module.daos.clear()
    yield
    daos_module.daos.clear()

@pytest.fixture
def client():
    """Provides a Flask test client for the application, with TESTING mode enabled."""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

# Helpers for integration tests

def create_user(client, email='test@example.com'):
    resp = client.post(
        '/users/create',
        data={'firstName': 'Test', 'lastName': 'User', 'email': email}
    )
    assert resp.status_code == 200
    return resp.get_json()['_id']['$oid']

def create_task(client, user_id):
    resp = client.post(
        '/tasks/create',
        data={
            'userid': user_id,
            'title': 'T',
            'description': 'D',
            'url': 'u',
            'todos': ['init']
        }
    )
    assert resp.status_code == 200
    return resp.get_json()[0]['_id']['$oid']

# Fixtures for integration tests

@pytest.fixture
def user_id(client):
    return create_user(client)

@pytest.fixture
def task_id(client, user_id):
    return create_task(client, user_id)