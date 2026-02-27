from app.core.celery import celery_app
from app.tasks.send_email import send_email

@celery_app.task
def send_task_assigned_email(user_email: str, task_title: str, assigned_by: str | None = None):
    subject = "New Task Assigned"

    body = f"""
You have been assigned a new task.

Task: {task_title}
Assigned by: {assigned_by or "Admin"}

Please check your dashboard.
"""

    send_email(user_email, subject, body)