"""
This module contains functional tests for the API endpoints that test negative scenarios.
"""
import pytest
import requests
from fastapi import status

from app.database.post import Post
from tests.functional.helpers import BASE_URL

pytestmark = pytest.mark.usefixtures("cleanup")


def test_create_post_real_request_both_link_and_text(
    db_session, test_error_data
):  # pylint: disable=redefined-outer-name
    """
    Test that verifies that a post cannot have both text and a link.
    """
    # When
    response = requests.post(
        f"{BASE_URL}/v1/post/",
        json=test_error_data,
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    # Then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    json_response = response.json()
    assert json_response["detail"][0]["loc"] == ["body", "link"]
    assert (
        json_response["detail"][0]["msg"]
        == "Value error, A post can have either text or a link, but not both"
    )

    post_in_db = db_session.query(Post).filter(Post.id == test_error_data["id"]).first()
    assert post_in_db is None
