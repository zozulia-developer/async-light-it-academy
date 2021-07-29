from pydantic import BaseModel
from typing import List, Dict, Any


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: Dict[str, Any]


class CreatePostParams(BaseModel):
    userId: int
    title: str
    body: str


class CreatedPost(BaseModel):
    userId: int
    id: int
    title: str
    body: str


class PostDetails(Post):
    comments: List[Dict[str, Any]]


class UpdatePostParams(BaseModel):
    title: str
    body: str
