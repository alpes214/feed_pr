from typing import Annotated, Optional

from fastapi import Depends

from app.configs.environment import EnvironmentSettings, get_environment_variables
from app.database.post import Post
from app.repositories.post_repository import PostRepository
from app.schemas.post_schema import PostSchema


class FeedUsecases:
    postRepository: PostRepository

    def __init__(
        self,
        postRepository: PostRepository = Depends(),
    ) -> None:
        self.postRepository = postRepository

    def post_create(self, post_body: PostSchema) -> Post:
        return self.postRepository.create(
            Post(
                id=post_body.id,
                title=post_body.title,
                author=post_body.author,
                text=post_body.text,
                link=str(post_body.link) if post_body.link else None,
                likes=post_body.likes,
                dislikes=post_body.dislikes,
                is_ad=post_body.is_ad,
                nsfw=post_body.nsfw,
                category=post_body.category,
            )
        )

    def post_get(self, post_id: str) -> Post:
        return self.postRepository.get(Post(id=post_id))

    def generate_feed(
        self,
        regular_posts: list[Post],
        ad_posts: list[Post],
        page: int,
        page_size: int,
        always_show_ads: bool,
        settings: Annotated[EnvironmentSettings, Depends(get_environment_variables)],
    ) -> list[Post]:
        start_idx = page * page_size
        end_idx = start_idx + page_size

        extracted_posts = regular_posts[start_idx:end_idx]

        def can_insert_ad(index: int) -> bool:
            # Check that index is in valid range
            if index < 0 or index > len(extracted_posts):
                return False

            # Check that index is not adjacent to NSFW post
            # also task casre about first and last post
            return (index == 0 or not extracted_posts[index - 1].nsfw) and (
                index == len(extracted_posts) or not extracted_posts[index].nsfw
            )

        def find_next_suitable_index(start_idx: int) -> int:
            idx = start_idx
            while idx < len(extracted_posts) and not can_insert_ad(idx):
                idx += 1
            return idx if idx < len(extracted_posts) else -1

        def insert_ad(target_idx: int):
            if always_show_ads:
                suitable_idx = find_next_suitable_index(target_idx)
                if suitable_idx != -1 and ad_posts:
                    extracted_posts.insert(suitable_idx, ad_posts.pop(0))
                    extracted_posts.pop()
            else:
                if can_insert_ad(target_idx) and ad_posts:
                    extracted_posts.insert(target_idx, ad_posts.pop(0))
                    extracted_posts.pop()

        if len(extracted_posts) > min(settings.APP_ADDS_POSITIONS):
            for idx in settings.APP_ADDS_POSITIONS:
                insert_ad(idx)

        return extracted_posts

    def post_list(
        self,
        start_index: Optional[
            int
        ] = get_environment_variables().APP_DEFAULT_START_INDEX,
        page_size: Optional[int] = get_environment_variables().APP_DEFAULT_PAGE_SIZE,
    ) -> (int, list[Post]):
        regular_count, regular_posts = self.postRepository.list_regular_posts(
            start_index, page_size
        )
        _, ads_posts = self.postRepository.list_ads_posts(start_index, page_size)
        feed = self.generate_feed(
            regular_posts,
            ads_posts,
            start_index,
            page_size,
            True,
            get_environment_variables(),
        )
        return regular_count, feed
