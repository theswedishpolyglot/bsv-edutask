import os
import pytest
from pymongo import MongoClient
from pymongo.errors import WriteError

from src.util.dao import DAO

@pytest.fixture(autouse=True)
def patch_getValidator(monkeypatch):
    """
    Replace both "src.util.validators.getValidator" and "src.util.dao.getValidator" 
    with a fake that only knows about "test_collection".
    """
    # Grab the real validators.getValidator
    from src.util.validators import getValidator as real_getValidator

    def fake_getValidator(collection_name: str):
        """
        A fake getValidator that returns a custom schema for "test_collection".

        Custom schema:
        - "name" is required (string)
        - "age" is optional (int)
        - "verified" is optional (bool)
        - "tags" is optional (array of strings, uniqueItems: true)
        """
        if collection_name == "test_collection":

            return {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["name"],
                    "properties": {
                        "name": { "bsonType": "string" },
                        "age": { "bsonType": "int" },
                        "verified": { "bsonType": "bool" },
                        "tags": {
                            "bsonType": "array",
                            "uniqueItems": True,
                            "items": { "bsonType": "string" }
                        }
                    }
                }
            }

        return real_getValidator(collection_name)

    monkeypatch.setattr("src.util.validators.getValidator", fake_getValidator)
    monkeypatch.setattr("src.util.dao.getValidator", fake_getValidator)

    yield

@pytest.fixture(scope="function")
def dao_custom():
    """
    Ensure the "test_collection" collection is dropped, then create a DAO pointing to it. 
    This collection will use the custom schema defined in the patched getValidator.
    After the test, the collection is dropped again.
    """
    # Connect to MongoDB
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    client = MongoClient(mongo_url)
    db = client["edutask"]

    # Drop the collection if it exists
    if "test_collection" in db.list_collection_names():
        db["test_collection"].drop()

    # Create the DAO for "test_collection"
    dao = DAO(collection_name="test_collection")

    yield dao

    # Tear down by dropping the collection
    db["test_collection"].drop()
    client.close()

### Integration tests for the DAO.create() method ###

def test_valid_insert(dao_custom):
    """
    This payload matches the custom schema perfectly, so insertion should succeed.
    """
    payload = {
        "name": "Tester",
        "age": 42,
        "verified": True
    }

    created = dao_custom.create(payload)
    assert "_id" in created
    assert created["name"] == "Tester"
    assert created["age"] == 42
    assert created["verified"] is True

def test_valid_insert_only_required(dao_custom):
    """
    This payload only includes the required "name" field, so it should succeed.
    """
    payload = { "name": "Tester" }
    created = dao_custom.create(payload)
    assert "_id" in created
    assert created["name"] == "Tester"
    assert "age" not in created
    assert "verified" not in created

def test_missing_required_name(dao_custom):
    """
    Omitting "name" entirely should violate the "required" constraint.
    The schema says "name" is required, so Mongo must reject this document.
    """
    payload = {
        "age": 12,
        "verified": False
    }
    with pytest.raises(WriteError):
        dao_custom.create(payload)

def test_wrong_type_name(dao_custom):
    """
    Setting "name" = 123 (an integer) violates the schema (must be a string).
    Mongo must reject this with a WriteError.
    """
    payload = {
        "name": 123, # wrong type
        "age": 456
    }
    with pytest.raises(WriteError):
        dao_custom.create(payload)

def test_wrong_type_verified(dao_custom):
    """
    Setting "verified" = "yes" (a string) violates the schema (must be a bool).
    Mongo must reject this with a WriteError.
    """
    payload = {
        "name": "Tester",
        "verified": "yes" # wrong type
    }
    with pytest.raises(WriteError):
        dao_custom.create(payload)

def test_wrong_type_inside_tags(dao_custom):
    """
    Setting "tags" = ["x", 5, "z"] violates the schema (must be an array of strings).
    Mongo must reject this with a WriteError.
    """
    payload = {
        "name": "Tester",
        "tags": ["x", 5, "z"]
    }
    with pytest.raises(WriteError):
        dao_custom.create(payload)

def test_uniqueitems_tags(dao_custom):
    """
    According to the docstring, "values of a property flagged with *uniqueItems*
    are unique among all documents of the collection." Therefore, inserting a second
    document with the same *tags* (property with uniqueItems flag) should raise a WriteError. 
    """
    payload1 = {
        "name": "Tester1",
        "tags": ["a", "b"]
    }
    created1 = dao_custom.create(payload1)
    assert "_id" in created1

    payload2 = {
        "name": "Tester2",
        "tags": ["a", "b"]
    }
    with pytest.raises(WriteError):
        dao_custom.create(payload2)
