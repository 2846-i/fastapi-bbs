from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, insert

from app.schemas.post import PostCreate, PostResponse
from app.database import get_db
from app.models.post import Post
from app.models.thread import Thread


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    stmt = select(Post).where(Post.id == post_id)
    post = db.execute(stmt).scalar_one_or_none()

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return post

threads_router = APIRouter(
    prefix="/threads",
    tags=["Posts"]
)

@threads_router.get("/{thread_id}/posts", response_model=list[PostResponse])
async def list_posts(thread_id: int, db: Session = Depends(get_db)):
    stmt_thread = select(Thread).where(Thread.id == thread_id)
    exists = db.execute(stmt_thread).scalar_one_or_none()

    if exists is None:
        raise HTTPException(status_code=404, detail="Thread not found")

    stmt = select(Post).where(Post.thread_id == thread_id).order_by(Post.post_number)
    posts = db.execute(stmt).scalars().all()

    return posts

@threads_router.post("/{thread_id}/posts", response_model=PostResponse)
async def create_post(thread_id: int, post: PostCreate, db: Session = Depends(get_db)):
    stmt_thread = select(Thread).where(Thread.id == thread_id)
    exists = db.execute(stmt_thread).scalar_one_or_none()

    if exists is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    stmt_last = (select(Post.post_number)
                .where(Post.thread_id == thread_id)
                .order_by(Post.post_number.desc())
                .limit(1)
    )

    last_number = db.execute(stmt_last).scalar_one_or_none()
    next_number = 1 if last_number is None else last_number + 1

    stmt_insert = insert(Post).values(
        thread_id = thread_id,
        post_number = next_number,
        content = post.content,
        parent_post_id = post.parent_post_id
    )

    result = db.execute(stmt_insert)

    db.commit()

    new_id = result.lastrowid

    stmt_new = select(Post).where(Post.id == new_id)
    new_post = db.execute(stmt_new).scalar_one()

    return new_post