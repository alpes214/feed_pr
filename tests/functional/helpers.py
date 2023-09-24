from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.configs.environment import get_environment_variables

env = get_environment_variables()
BASE_URL = f"http://{env.TEST_WEB_APP_HOST}:8000"
engine = create_engine(env.DATABASE_URL)
TestSession = sessionmaker(autocommit=False, autoflush=True, bind=engine)


def assert_post_data(json_response, expected_data):
    """
    Asserts that the given JSON response matches the expected data.
    """
    assert json_response is not None
    assert expected_data is not None
    assert str(json_response["id"]) == expected_data["id"]
    assert json_response["title"] == expected_data["title"]
    assert json_response["author"] == expected_data["author"]
    assert json_response["text"] == expected_data["text"]
    assert json_response["link"] is None
    assert json_response["likes"] == expected_data["likes"]
    assert json_response["dislikes"] == expected_data["dislikes"]
    assert json_response["is_ad"] == expected_data["is_ad"]
    assert json_response["nsfw"] == expected_data["nsfw"]
    assert json_response["category"] == expected_data["category"]


def assert_post_in_db(post_in_db, new_post_data):
    """
    Asserts that the given post is in the database and has the expected data.
    """
    assert post_in_db is not None
    assert new_post_data is not None
    assert_post_data(post_in_db.as_dict(), new_post_data)
    assert post_in_db.score == new_post_data["likes"] - new_post_data["dislikes"]
    assert str(post_in_db) == (
        f"<Post(id='{new_post_data['id']}', is_ad={new_post_data['is_ad']}, "
        f"nsfw={new_post_data['nsfw']})>"
    )
