from unittest import TestCase
from unittest.mock import create_autospec, patch

from app.configs.environment import get_environment_variables
from app.database.post import Post
from app.repositories.post_repository import PostRepository
from app.usecases.feed_usecases import FeedUsecases

env = get_environment_variables()


class TestFeed(TestCase):
    postRepository: PostRepository
    feedUsecase: FeedUsecases

    def setUp(self):
        super().setUp()
        self.postRepository = create_autospec(PostRepository)
        self.feedUsecase = FeedUsecases(self.postRepository)

    @patch(
        "app.schemas.post_schema.PostSchema",
    )
    def test_create(self, PostSchema):
        post = PostSchema()
        post.title = "Worker cold exist pull glass me yeah."
        post.author = "Linda"
        post.text = """
            Drug moment use role seem. You anything claim certainly to participant. 
            Capital majority speak structure.
            Provide main cold. One enjoy radio central including.
        """
        post.link = "http://fields.org/"
        post.likes = 5710
        post.dislikes = 2992
        post.is_ad = False
        post.nsfw = False

        self.feedUsecase.post_create(post)

        # Should call create method on PostRepository
        self.postRepository.create.assert_called_once()

    def test_form_feed_without_nsf(self):
        regualar_posts = [
            Post(id=f"{index}", is_ad=False, nsfw=False)
            for index in range(env.APP_DEFAULT_PAGE_SIZE)
        ]
        ads_posts = [
            Post(id="a", is_ad=True, nsfw=False),
            Post(id="b", is_ad=True, nsfw=False),
        ]

        result_posts = self.feedUsecase.generate_feed(
            regualar_posts.copy(),
            ads_posts.copy(),
            0,
            env.APP_DEFAULT_PAGE_SIZE,
            True,
            env,
        )

        self.assertEqual(result_posts[env.APP_ADDS_POSITIONS[0]].id, "a")
        self.assertEqual(result_posts[env.APP_ADDS_POSITIONS[1]].id, "b")

        regular_idx = [
            idx
            for idx in range(env.APP_DEFAULT_PAGE_SIZE)
            if idx != env.APP_ADDS_POSITIONS[0] and idx != env.APP_ADDS_POSITIONS[1]
        ]
        for idx in regular_idx:
            self.assertFalse(result_posts[idx].is_ad)

        for idx, p in enumerate(result_posts):
            if p.is_ad:
                self.assertFalse(result_posts[idx - 1].nsfw)
                self.assertFalse(result_posts[idx + 1].nsfw)

    def test_form_feed_with_nsfw_on_ads_places(self):
        # generate feed for regular posts with default page size
        regualar_posts = [
            Post(id=f"{index}", is_ad=False, nsfw=False)
            for index in range(env.APP_DEFAULT_PAGE_SIZE)
        ]

        # set nsfw to be adjacent to ad places
        regualar_posts[env.APP_ADDS_POSITIONS[0]].nsfw = True
        # second ad place will be shifted by inserting first ad
        regualar_posts[env.APP_ADDS_POSITIONS[1] - 1].nsfw = True

        # predefined list of ads
        ads_posts = [
            Post(id="a", is_ad=True, nsfw=False),
            Post(id="b", is_ad=True, nsfw=False),
        ]

        # joining regular and ads posts and generating feed
        result_posts = self.feedUsecase.generate_feed(
            regualar_posts.copy(),
            ads_posts.copy(),
            0,
            env.APP_DEFAULT_PAGE_SIZE,
            True,
            env,
        )

        # check that ads are on correct places
        self.assertEqual(result_posts[env.APP_ADDS_POSITIONS[0] + 2].id, "a")
        self.assertEqual(result_posts[env.APP_ADDS_POSITIONS[1] + 2].id, "b")

        # check that len of the resul feed is not changed
        self.assertEqual(len(result_posts), env.APP_DEFAULT_PAGE_SIZE)

        # check that regular posts are not changed
        regular_idx = [
            idx
            for idx in range(env.APP_DEFAULT_PAGE_SIZE)
            if idx != env.APP_ADDS_POSITIONS[0] + 2
            and idx != env.APP_ADDS_POSITIONS[1] + 2
        ]
        for idx in regular_idx:
            self.assertFalse(result_posts[idx].is_ad)

        # check that nsfw posts are not adjacent to ads
        for idx, p in enumerate(result_posts):
            if p.is_ad:
                self.assertFalse(result_posts[idx - 1].nsfw)
                self.assertFalse(result_posts[idx + 1].nsfw)

    def test_form_feed_with_empty_lists(self):
        regualar_posts = []
        ads_posts = []

        result_posts = self.feedUsecase.generate_feed(
            regualar_posts.copy(),
            ads_posts.copy(),
            0,
            env.APP_DEFAULT_PAGE_SIZE,
            True,
            env,
        )

        self.assertEqual(len(result_posts), 0)
