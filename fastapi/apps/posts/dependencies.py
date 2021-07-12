import aiohttp

from typing import List, Dict, Any, Coroutine

from .models import Post, CreatePostParams


class PostRepository:
    def __init__(self):
        self._posts: List[Post] = []

    async def create_post(self, post: CreatePostParams) -> Post:
        pass

    async def list_posts(self) -> List[Post]:
        return self._posts.copy()


class JSONPlaceholderPostRepository(PostRepository):
    def __init__(self):
        self._endpoint = "https://jsonplaceholder.typicode.com/posts"
        self._endpoint_author = "https://jsonplaceholder.typicode.com/users"

    async def list_posts(self) -> List[Coroutine[Any, Any, Post]]:
        raw_posts = await self._list_posts()
        return [self._convert_post(raw_post) for raw_post in raw_posts]

    async def _list_posts(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self._endpoint)
            raw_posts = await resp.json()
            return raw_posts

    async def _convert_post(self, raw_post: Dict[str, Any]) -> Post:
        return Post(**raw_post)


class PostRepositoryFactory:
    def __init__(self):
        self._repo = None

    def __call__(self) -> PostRepository:
        if self._repo is None:
            self._repo = JSONPlaceholderPostRepository()
        return self._repo


get_post_repository = PostRepositoryFactory()