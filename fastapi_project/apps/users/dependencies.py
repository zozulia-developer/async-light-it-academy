from typing import List, Dict, Any

import aiohttp
from fastapi import Depends

from .models import CreateUserParams, User


async def get_session() -> aiohttp.ClientSession:
    async with aiohttp.ClientSession(trust_env=True) as session:
        yield session


class UserRepository:
    def __init__(self, session) -> None:
        self._users: List[User] = []
        self._serial = len(self._users)
        self._session = session

    async def create_user(self, user: CreateUserParams) -> User:
        user = User(id=self._serial, **user.dict())
        self._serial += 1
        self._users.append(user)
        return user

    async def list_users(self) -> List[User]:
        return self._users.copy()


class JSONPlaceholderUserRepository(UserRepository):
    def __init__(self, session):
        self._endpoint = "https://jsonplaceholder.typicode.com/users"
        self._session = session

    async def create_user(self, user: CreateUserParams) -> User:
        raw_user = await self._create_user(user)
        return self._convert_user(raw_user)

    async def list_users(self) -> List[User]:
        raw_users = await self._list_users()
        return [self._convert_user(raw_user) for raw_user in raw_users]

    async def _create_user(self, user: CreateUserParams) -> Dict[str, Any]:
        resp = await self._session.post(self._endpoint, json=user.dict())
        raw_user = await resp.json()
        return raw_user

    async def _list_users(self) -> List[Dict[str, Any]]:
        resp = await self._session.get(self._endpoint)
        raw_users = await resp.json()
        return raw_users

    def _convert_user(self, raw_user: Dict[str, Any]) -> User:
        return User(**raw_user)


class UserRepositoryFactory:
    def __init__(self):
        self._repo = None

    def __call__(self, session: aiohttp.ClientSession = Depends(get_session)) -> UserRepository:
        _repo = JSONPlaceholderUserRepository(session)
        return _repo


get_user_repository = UserRepositoryFactory()
