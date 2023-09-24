"""Data migration

Revision ID: 3820bc6ad5c4
Revises: 2d5bd0f810f6
Create Date: 2023-09-14 20:27:19.643951

"""
import uuid
from random import choice
from alembic import op
import sqlalchemy as sa
from faker import Faker

faker = Faker()

# revision identifiers, used by Alembic.
revision = "3820bc6ad5c4"
down_revision = "2d5bd0f810f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("TRUNCATE TABLE posts CASCADE;")
    op.execute("commit;")

    # Insert new records into the 'posts' table
    uuid_post = [uuid.uuid4() for _ in range(100)]
    text_or_link = [faker.boolean() for _ in range(100)]

    categories = (
        "IT",
        "Politics",
        "Fashion",
        "Games",
        "Sports",
        "Home",
        "Health",
        "Travelling",
    )
    for i in range(100):
        op.execute(
            f"""
                INSERT INTO posts(id, title, author, {'link' if text_or_link[i] else 'text'}, category, likes, dislikes, is_ad, nsfw) 
                VALUES (
                '{uuid_post[i]}',
                '{faker.sentence(4)}',
                '{faker.pystr(min_chars=10, max_chars=10).lower()}',
                '{faker.url() if text_or_link[i] else faker.text()}',
                '{choice(categories)}',
                {faker.random_int()},
                {faker.random_int()},
                {True if i%7 == 0 else False},
                {True if i%11 == 0 else False});"""
        )
    op.execute("commit;")


def downgrade() -> None:
    op.execute("TRUNCATE TABLE posts CASCADE;")
