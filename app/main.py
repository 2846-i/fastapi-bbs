from fastapi import FastAPI

from app.routers import threads
from app.routers import posts

app = FastAPI()

app.include_router(threads.router)
app.include_router(posts.router)
app.include_router(posts.threads_router)
