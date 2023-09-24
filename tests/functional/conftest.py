import uuid

import pytest
from faker import Faker

from app.database.base_model import EntityMeta
from tests.functional.helpers import TestSession


def db_cleanup():
    """
    Cleans up the database by deleting all records from all tables.
    """
    session = TestSession()

    for table in reversed(EntityMeta.metadata.sorted_tables):
        session.execute(table.delete())

    session.commit()
    session.close()


@pytest.fixture(scope="function", autouse=True)
def db_session():
    """
    This function creates a new database session for testing purposes.
    It begins a nested transaction, yields the session object, and rolls back the transaction
    after the test is complete.
    """
    session = TestSession()
    session.begin_nested()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def cleanup():
    """
    A fixture that cleans up the database after a test is done using it.
    """
    yield
    db_cleanup()


@pytest.fixture(scope="function", autouse=True)
def test_data():
    """
    Returns a dictionary containing fake data for testing purposes.
    """
    faker = Faker()
    return {
        "id": f"{uuid.uuid4()}",
        "title": faker.sentence(4),
        "author": faker.pystr(min_chars=10, max_chars=10).lower(),
        "text": faker.text(),
        "likes": faker.random_int(),
        "dislikes": faker.random_int(),
        "is_ad": False,
        "nsfw": True,
        "category": "IT",
    }


@pytest.fixture(scope="function", autouse=True)
def test_error_data():
    """
    Returns a dictionary containing fake data for testing purposes.
    """
    faker = Faker()
    return {
        "id": f"{uuid.uuid4()}",
        "title": faker.sentence(4),
        "author": faker.pystr(min_chars=10, max_chars=10).lower(),
        "text": faker.text(),
        "link": faker.url(),
        "likes": faker.random_int(),
        "dislikes": faker.random_int(),
        "is_ad": False,
        "nsfw": True,
        "category": "IT",
    }
