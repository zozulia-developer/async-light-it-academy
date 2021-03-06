import aiohttp
from aiohttp import ClientSession

from typing import List, Dict, Any

from fastapi import Depends

from .models import Post, CreatePostParams, CreatedPost, PostDetails, UpdatePostParams


async def get_session() -> ClientSession:
    async with ClientSession(trust_env=True) as session:
        yield session


class PostRepository:
    def __init__(self, session) -> None:
        self._endpoint_posts = "https://jsonplaceholder.typicode.com/posts"
        self._endpoint_users = "https://jsonplaceholder.typicode.com/users"
        self._endpoint_comments = "https://jsonplaceholder.typicode.com/comments"
        self._session = session

    async def list_posts(self) -> List[Post]:
        raw_posts = await self._list_posts()
        raw_users = await self._list_users()
        for post in raw_posts:
            author = [user for user in raw_users if user['id'] == post['userId']][0]
            post['author'] = {
                'id': author['id'],
                'name': author['name'],
                'email': author['email']
            }
        return [self._convert_post(raw_post) for raw_post in raw_posts]

    async def create_post(self, post: CreatePostParams):
        raw_post = await self._create_post(post)
        return self._convert_created_post(raw_post)

    async def update_post(self, post: UpdatePostParams, post_id: int) -> Dict[str, Any]:
        raw_post = await self._update_post(post, post_id)
        return raw_post

    async def post_details(self, post_id: int) -> PostDetails:
        raw_post = await self._post_details(post_id)
        return self._convert_post_details(raw_post)

    async def _list_posts(self) -> List[Dict[str, Any]]:
        resp_posts = await self._session.get(self._endpoint_posts)
        raw_posts = await resp_posts.json()
        return raw_posts

    async def _post_details(self, post_id: int) -> Dict[str, Any]:
        resp = await self._session.get(f'{self._endpoint_posts}/{post_id}')
        raw_post = await resp.json()
        resp_comments = await self._session.get(f"{self._endpoint_comments}?postId={post_id}")
        raw_comments = await resp_comments.json()
        resp_user = await self._session.get(f"{self._endpoint_users}/{raw_post['userId']}")
        raw_user = await resp_user.json()
        raw_post['author'] = {
            'id': raw_user['id'],
            'name': raw_user['name'],
            'email': raw_user['email']
        }
        raw_post['comments'] = raw_comments
        return raw_post

    async def _list_users(self) -> List[Dict[str, Any]]:
        resp = await self._session.get(self._endpoint_users)
        raw_users = await resp.json()
        return raw_users

    async def _list_comments(self) -> List[Dict[str, Any]]:
        resp = await self._session.get(self._endpoint_comments)
        raw_comments = await resp.json()
        return raw_comments

    async def _create_post(self, user: CreatePostParams) -> Dict[str, Any]:
        resp = await self._session.post(self._endpoint_posts, json=user.dict())
        raw_post = await resp.json()
        return raw_post

    async def _update_post(self, post: UpdatePostParams, post_id: int) -> Dict[str, Any]:
        resp = await self._session.put(
            f'{self._endpoint_posts}/{post_id}',
            json=post.dict()
        )
        raw_post = await resp.json()
        return raw_post

    def _convert_post(self, raw_post: Dict[str, Any]) -> Post:
        return Post(**raw_post)

    def _convert_created_post(self, raw_post: Dict[str, Any]) -> CreatedPost:
        return CreatedPost(**raw_post)

    def _convert_post_details(self, raw_post: Dict[str, Any]) -> PostDetails:
        return PostDetails(**raw_post)


class PostRepositoryFactory:
    def __init__(self):
        self._repo = None

    def __call__(self, session: ClientSession = Depends(get_session)) -> PostRepository:
        _repo = PostRepository(session)
        return _repo


get_post_repository = PostRepositoryFactory()
