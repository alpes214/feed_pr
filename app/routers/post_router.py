from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.configs.database import SessionLocal
from app.repositories import post_repository
from app.schemas.post_schema import PaginatedPostResponse, PostSchema
from app.usecases.feed_usecases import FeedUsecases

PostRouter = APIRouter(prefix="/v1", tags=["post"])


def get_feed_use_case():
    db = SessionLocal()
    postRepository = post_repository.PostRepository(db=db)
    return FeedUsecases(postRepository=postRepository)


@PostRouter.get("/posts/", response_model=PaginatedPostResponse)
def index(
    page: Annotated[int, Query(ge=0)] = 0,
    pageSize: Annotated[int, Query(ge=1, le=50)] = 25,
    feedUsecases: FeedUsecases = Depends(get_feed_use_case),
):
    count, results = feedUsecases.post_list(page, pageSize)
    return PaginatedPostResponse(
        status=200, page=page, pageSize=pageSize, totalItems=count, data=results
    )


@PostRouter.get("/post/{id}", response_model=PostSchema)
def get(
    id: str,
    feedUsecases: FeedUsecases = Depends(get_feed_use_case),
):
    post = feedUsecases.post_get(post_id=id)
    return PostSchema.model_validate(post)


@PostRouter.post(
    "/post/",
    response_model=PostSchema,
    status_code=status.HTTP_201_CREATED,
)
def create(post: PostSchema, feedUsecases: FeedUsecases = Depends(get_feed_use_case)):
    post = feedUsecases.post_create(post)
    return PostSchema.model_validate(post)
