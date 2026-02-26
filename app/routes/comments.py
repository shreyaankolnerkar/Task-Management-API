from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.authentication.dependencies import get_current_user
from app.db.models import Comment, Task
from app.db.session import get_db

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/")
def add_comment(
    task_id: int,
    content: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    comment = Comment(
        content=content,
        task_id=task_id,
        user_id=user.id,
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment
