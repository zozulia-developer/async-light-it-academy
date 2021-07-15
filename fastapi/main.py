import uvicorn
from fastapi import FastAPI


from apps import users, posts


def create_app():
    app = FastAPI()
    app.include_router(users.router, prefix="/users")
    app.include_router(posts.router, prefix="/posts")
    return app


app = create_app()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
