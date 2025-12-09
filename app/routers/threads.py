from fastapi import APIRouter
from app.schemas.thread import ThreadResponse, ThreadCreate
from datetime import datetime

router = APIRouter(
    prefix="/threads",
    tags=["Threads"]
)

@router.get("/", response_model=list[ThreadResponse])
async def list_threads():
    return [
        {"id": 1, "title": "ダミースレッド1", "created_at": "2025-11-20T00:00:00"},
        {"id": 2, "title": "ダミースレッド2", "created_at": "2025-11-21T00:00:00"},
    ]

@router.get("/{thread_id}", response_model=ThreadResponse)
async def get_thread(thread_id: int):
    return {
        "id": thread_id,
        "title": f"ダミースレッド{thread_id}",
        "created_at": "2025-11-21T00:00:00"
    }

@router.post("/", response_model=ThreadResponse)
async def create_thread(thread: ThreadCreate):
    return {
        "id": 999,
        "title": thread.title,
        "created_at": "2025-11-21T00:00:00",
    }
