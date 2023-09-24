import uuid
from typing import List, Optional

from faker import Faker
from pydantic import UUID4, BaseModel, ConfigDict, Field, HttpUrl, validator

faker = Faker()


class PostSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[UUID4] = Field(
        examples=[uuid.uuid4() for a in range(10)], default=None
    )
    title: str = Field(examples=[faker.sentence(4) for a in range(10)])
    author: str = Field(
        max_length=10,
        min_length=10,
        description="Author name with alphanumeric characters in lowercase with maximum 10 characters",
        examples=[faker.pystr(min_chars=10, max_chars=10).lower() for a in range(10)],
    )
    text: Optional[str] = Field(
        examples=[faker.text() for _ in range(10)], default=None
    )
    link: Optional[HttpUrl] = Field(
        examples=[faker.url() for _ in range(10)], default=None
    )
    likes: Optional[int] = Field(
        ge=0, examples=[faker.random_int() for _ in range(10)], default=None
    )
    dislikes: Optional[int] = Field(
        ge=0, examples=[faker.random_int() for _ in range(10)], default=None
    )
    is_ad: Optional[bool] = Field(
        examples=[faker.boolean() for _ in range(10)], default=None
    )
    nsfw: Optional[bool] = Field(
        examples=[faker.boolean() for _ in range(10)], default=None
    )
    category: Optional[str] = None

    @validator("author")
    def validate_author(cls, value):
        if not value.isalnum() or not value.islower():
            raise ValueError(
                "Author name must contain only alphanumeric characters in lowercase"
            )
        return value

    @validator("text", pre=True, always=True)
    def validate_text_or_link_1(cls, text, values):
        link = values.get("link")
        if text is not None and link is not None:
            raise ValueError("A post can have either text or a link, but not both")
        return text

    @validator("link", pre=True, always=True)
    def validate_text_or_link_2(cls, link, values):
        text = values.get("text")
        if link is not None and text is not None:
            raise ValueError("A post can have either text or a link, but not both")
        return link


class PaginatedPostResponse(BaseModel):
    status: int
    page: int
    pageSize: int
    totalItems: int
    data: List[PostSchema]
