"""
This module contains positive functional tests for the API endpoints of the feed application.

The tests cover the creation of posts, retrieval of posts, and pagination of posts.
"""
import uuid

import pytest
import requests
from fastapi import status

from app.database.post import Post
from tests.functional.helpers import BASE_URL, assert_post_data, assert_post_in_db

pytestmark = pytest.mark.usefixtures("cleanup")


def test_create_post(db_session, test_data):  # pylint: disable=redefined-outer-name
    """
    Test creating a new post and checking if it was added to the database correctly.
    """
    # When
    response = requests.post(
        f"{BASE_URL}/v1/post/",
        json=test_data,
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    # Then
    assert response.status_code == status.HTTP_201_CREATED
    assert_post_data(response.json(), test_data)

    post_in_db = db_session.query(Post).filter(Post.id == test_data["id"]).first()
    assert_post_in_db(post_in_db, test_data)


def test_create_post_check_get(test_data):  # pylint: disable=redefined-outer-name
    """
    Test creating a new post and then retrieving it to ensure it was created correctly.
    """
    # When
    response = requests.post(
        f"{BASE_URL}/v1/post/",
        json=test_data,
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    # Then
    assert response.status_code == status.HTTP_201_CREATED
    assert_post_data(response.json(), test_data)

    response = requests.get(
        f"{BASE_URL}/v1/post/{test_data['id']}",
        timeout=5,
    )

    assert response.status_code == status.HTTP_200_OK
    assert_post_data(response.json(), test_data)


def test_create_post_check_get_and_list(
    test_data,
):  # pylint: disable=redefined-outer-name
    """
    Test function to create a post, check if it can be retrieved and listed.
    """
    # Given
    response = requests.post(
        f"{BASE_URL}/v1/post/",
        json=test_data,
        headers={"Content-Type": "application/json"},
        timeout=5,
    )
    assert response.status_code == status.HTTP_201_CREATED

    # When
    response = requests.get(
        f"{BASE_URL}/v1/posts/?page=0&pageSize=25",
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get("data", [])) == 1
    assert_post_data(response.json().get("data", [])[0], test_data)

    response = requests.get(
        f"{BASE_URL}/v1/post/{test_data['id']}",
        timeout=5,
    )
    assert response.status_code == status.HTTP_200_OK
    assert_post_data(response.json(), test_data)


def test_create_post_check_pagination(
    test_data,  # pylint: disable=redefined-outer-name
):
    """
    Test case to verify that posts are created and pagination is working as expected.
    """
    # Given
    ids = [uuid.uuid4() for _ in range(35)]

    for _, uid in enumerate(ids):
        test_data["id"] = f"{uid}"

        response = requests.post(
            f"{BASE_URL}/v1/post/",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
        assert response.status_code == status.HTTP_201_CREATED

    # When
    response = requests.get(
        f"{BASE_URL}/v1/posts/?page=0&pageSize=25",
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get("data", [])) == 25
