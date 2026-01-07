
from fastapi import APIRouter,Depends
from app.models.thread import Thread
from app.schemas.thread import ThreadResponse, ThreadCreate
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select, insert

router = APIRouter(
    prefix="/threads",
    tags=["Threads"]
)

@router.get("/", response_model=list[ThreadResponse])
async def list_threads(db: Session = Depends(get_db)):
    stmt = select(Thread)
    result = db.execute(stmt).scalars().all()
    return result

@router.get("/{thread_id}", response_model=ThreadResponse)
async def get_thread(thread_id: int, db: Session = Depends(get_db)):
    stmt = select(Thread).where(Thread.id == thread_id)
    result = db.execute(stmt).scalar_one()
    return result

@router.post("/", response_model=ThreadResponse)
async def create_thread(thread: ThreadCreate,db: Session = Depends(get_db)):
    stmt = insert(Thread).values(title=thread.title)
    result = db.execute(stmt)
    db.commit()

    new_id = result.lastrowid

    stmt2 = select(Thread).where(Thread.id == new_id)
    new_thread = db.execute(stmt2).scalar_one()
    return new_thread