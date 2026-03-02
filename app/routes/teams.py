from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.authentication.dependencies import get_current_user
from app.authentication.permissions import require_team_admin
from app.db.models import Team,User
from app.db.session import get_db

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/")
def create_team(
    name: str, user=Depends(get_current_user), db: Session = Depends(get_db)
):
    team = Team(name=name, owner_id=user.id)
    db.add(team)
    db.commit()
    return {"msg": "Team created"}


@router.post("/{team_id}/add-member")
def add_member(
    team_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)
):
    require_team_admin(team_id, user, db)
    team = db.query(Team).filter(Team.id == team_id).first()
    new_member = db.query(User).filter(User.id == user.id).first()
    team.members.append(new_member) 
    db.commit() 
    return {"msg": "Member added"}
