import uuid
from unittest import TestCase

from faker import Faker
from pydantic import ValidationError

from app.schemas.post_schema import PostSchema

faker = Faker()


class TestPostSchema(TestCase):
    def test_uuid_validation(self):
        with self.assertRaisesRegex(ValidationError, "Input should be a valid UUID"):
            PostSchema(
                id="123",
                title=faker.sentence(4),
                author=faker.pystr(min_chars=10, max_chars=10).lower(),
                text=faker.text(),
                likes=faker.random_int(),
                dislikes=faker.random_int(),
                is_ad=faker.boolean(),
                nsfw=faker.boolean(),
                category=faker.word(),
            )

    def test_title_validation(self):
        with self.assertRaisesRegex(ValidationError, "Field required"):
            PostSchema(
                id=uuid.uuid4(),
                author=faker.pystr(min_chars=10, max_chars=10).lower(),
                text=faker.text(),
                likes=faker.random_int(),
                dislikes=faker.random_int(),
                is_ad=faker.boolean(),
                nsfw=faker.boolean(),
                category=faker.word(),
            )

    def test_link_text_validation(self):
        with self.assertRaisesRegex(
            ValidationError, "A post can have either text or a link, but not both"
        ):
            PostSchema(
                id=uuid.uuid4(),
                title=faker.sentence(4),
                author=faker.pystr(min_chars=10, max_chars=10).lower(),
                text=faker.text(),
                link=faker.url(),
                likes=faker.random_int(),
                dislikes=faker.random_int(),
                is_ad=faker.boolean(),
                nsfw=faker.boolean(),
                category=faker.word(),
            )

    def test_author_validation(self):
        with self.assertRaisesRegex(
            ValidationError, "String should have at least 10 characters"
        ):
            PostSchema(
                id=uuid.uuid4(),
                title=faker.sentence(4),
                author="A",
                text=faker.text(),
                likes=faker.random_int(),
                dislikes=faker.random_int(),
                is_ad=faker.boolean(),
                nsfw=faker.boolean(),
                category=faker.word(),
            )

        with self.assertRaisesRegex(
            ValidationError, "String should have at most 10 characters"
        ):
            PostSchema(
                id=uuid.uuid4(),
                title=faker.sentence(4),
                author="01234567890",
                text=faker.text(),
                likes=faker.random_int(),
                dislikes=faker.random_int(),
                is_ad=faker.boolean(),
                nsfw=faker.boolean(),
                category=faker.word(),
            )

        with self.assertRaisesRegex(
            ValidationError,
            "Author name must contain only alphanumeric characters in lowercase",
        ):
            PostSchema(
                id=uuid.uuid4(),
                title=faker.sentence(4),
                author="012345678#",
                text=faker.text(),
                likes=faker.random_int(),
                dislikes=faker.random_int(),
                is_ad=faker.boolean(),
                nsfw=faker.boolean(),
                category=faker.word(),
            )

        with self.assertRaisesRegex(
            ValidationError,
            "Author name must contain only alphanumeric characters in lowercase",
        ):
            PostSchema(
                id=uuid.uuid4(),
                title=faker.sentence(4),
                author="012345678A",
                text=faker.text(),
                likes=faker.random_int(),
                dislikes=faker.random_int(),
                is_ad=faker.boolean(),
                nsfw=faker.boolean(),
                category=faker.word(),
            )

        with self.assertRaisesRegex(ValidationError, "Field required"):
            PostSchema(
                id=uuid.uuid4(),
                title=faker.sentence(4),
                text=faker.text(),
                likes=faker.random_int(),
                dislikes=faker.random_int(),
                is_ad=faker.boolean(),
                nsfw=faker.boolean(),
                category=faker.word(),
            )

    def test_likes_validation(self):
        with self.assertRaisesRegex(
            ValidationError,
            "Input should be a valid integer, unable to parse string as an integer",
        ):
            PostSchema(
                id=uuid.uuid4(),
                title=faker.sentence(4),
                author=faker.pystr(min_chars=10, max_chars=10).lower(),
                text=faker.text(),
                likes="aaaaaaa",
                dislikes=faker.random_int(),
                is_ad=faker.boolean(),
                nsfw=faker.boolean(),
                category=faker.word(),
            )

        with self.assertRaisesRegex(
            ValidationError, "Input should be greater than or equal to 0"
        ):
            PostSchema(
                id=uuid.uuid4(),
                title=faker.sentence(4),
                author=faker.pystr(min_chars=10, max_chars=10).lower(),
                text=faker.text(),
                likes=-1,
                dislikes=faker.random_int(),
                is_ad=faker.boolean(),
                nsfw=faker.boolean(),
                category=faker.word(),
            )

    def test_dislikes_validation(self):
        with self.assertRaisesRegex(
            ValidationError,
            "Input should be a valid integer, unable to parse string as an integer",
        ):
            PostSchema(
                id=uuid.uuid4(),
                title=faker.sentence(4),
                author=faker.pystr(min_chars=10, max_chars=10).lower(),
                text=faker.text(),
                likes=1,
                dislikes="aaaaaaa",
                is_ad=faker.boolean(),
                nsfw=faker.boolean(),
                category=faker.word(),
            )

        with self.assertRaisesRegex(
            ValidationError, "Input should be greater than or equal to 0"
        ):
            PostSchema(
                id=uuid.uuid4(),
                title=faker.sentence(4),
                author=faker.pystr(min_chars=10, max_chars=10).lower(),
                text=faker.text(),
                likes=1,
                dislikes=-1,
                is_ad=faker.boolean(),
                nsfw=faker.boolean(),
                category=faker.word(),
            )
