from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.authentication.permissions import require_admin
from app.db.models import Task, User
from app.db.session import get_db
from app.tasks.email_tasks import send_task_assigned_email

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/")
def create_task(
    title: str,
    team_id: int,
    description: str | None ,
    priority: str | None,
    due_date: datetime | None,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    task = Task(
        title=title,
        team_id=team_id,
        description=description,
        priority=priority,
        due_date=due_date,
        status="todo",
        created_by=admin.id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.put("/{task_id}")
def update_task(
    task_id: int,
    title: str | None,
    description: str | None,
    status: str | None,
    priority: str | None,
    due_date: datetime | None,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(404, "Task not found")

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if status is not None:
        task.status = status
    if priority is not None:
        task.priority = priority
    if due_date is not None:
        task.due_date = due_date

    db.commit()
    db.refresh(task)

    return task


@router.put("/{task_id}/assign")
def assign_task(
    task_id: int,
    assigned_to: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    
    assignee = db.get(User, assigned_to)
    if not assignee:
        raise HTTPException(404, "User not found")


    task.assigned_to = assigned_to
    db.commit()
    db.refresh(task)

    
    send_task_assigned_email.delay(
        assignee.email,   
        task.title,       
        admin.name if hasattr(admin, "name") else "Admin"
    )

    return {"message": "Task assigned & email sent"}


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(404, "Task not found")

    db.delete(task)
    db.commit()

    return {"msg": "Task deleted"}
