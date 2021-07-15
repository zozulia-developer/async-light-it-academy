from pydantic import BaseModel
from typing import List, Dict, Any


class Post(BaseModel):
    id: int
    title: str
    body: str
    # author: Dict[str, Any]


class CreatePostParams(BaseModel):
    author_id: int
    title: str
    body: str


class DetailPost(Post):
    id: int
    title: str
    body: str
    author: Dict[str, Any]
    comments: List[Dict[str, Any]]


class UpdatePostParams(BaseModel):
    title: str
    body: str
