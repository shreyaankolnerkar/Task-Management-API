from fastapi import FastAPI

from app.db.models import Base
from app.db.session import engine
from app.routes import comments, tasks, teams, users

app = FastAPI(title="Task Manager")

Base.metadata.create_all(bind=engine)


app.include_router(users.router)
app.include_router(teams.router)
app.include_router(tasks.router)
app.include_router(comments.router)
