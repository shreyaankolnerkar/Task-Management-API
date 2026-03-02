from celery import Celery
import os
from dotenv import load_dotenv
load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")
 
celery_app = Celery(
    "task_management",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks.email_tasks"], 
)

