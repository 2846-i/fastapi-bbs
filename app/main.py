from fastapi import FastAPI
from app.routers import threads

app = FastAPI(title="BBS API - Step1")

# ルーターを登録（まだ中身は空でOK）
app.include_router(threads.router)
