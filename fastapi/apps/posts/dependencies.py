import aiohttp

from typing import List, Dict, Any, Coroutine

from .models import Post, CreatePostParams


class PostRepository:
    def __init__(self):
        self._endpoint_posts = "https://jsonplaceholder.typicode.com/posts"
        self._endpoint_users = "https://jsonplaceholder.typicode.com/users"
        self._endpoint_comments = "https://jsonplaceholder.typicode.com/comments"

    async def list_posts(self) -> List[Post]:
        raw_posts = await self._list_posts()
        raw_users = await self._list_users()
        return [self._convert_post(raw_post) for raw_post in raw_posts]

    async def create_post(self, post: CreatePostParams) -> Coroutine[Any, Any, Post]:
        raw_post = await self._create_post(post)
        return self._convert_post(raw_post)

    async def _list_posts(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession(trust_env=True) as session:
            resp_posts = await session.get(self._endpoint_posts)
            raw_posts = await resp_posts.json()
            return raw_posts

    async def _list_users(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession(trust_env=True) as session:
            resp = await session.get(self._endpoint_users)
            raw_users = await resp.json()
            return raw_users

    async def _get_author_by_user_id(self, user_id: int) -> Dict[str, Any]:
        pass

    async def _list_comments(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self._endpoint_comments)
            raw_comments = await resp.json()
            return raw_comments

    async def _convert_post(self, raw_post: Dict[str, Any]) -> Post:
        return Post(**raw_post)


class PostRepositoryFactory:
    def __init__(self):
        self._repo = None

    def __call__(self) -> PostRepository:
        if self._repo is None:
            self._repo = PostRepository()
        return self._repo


get_post_repository = PostRepositoryFactory()
