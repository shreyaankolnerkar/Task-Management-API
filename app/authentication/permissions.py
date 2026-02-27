from fastapi import HTTPException,Depends

from app.db.models import Team, User
from app.authentication.dependencies import get_current_user


def require_admin(user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    return user


def require_team_admin(team_id: int, user: User, db):
    team = db.get(Team, team_id)

    if not team:
        raise HTTPException(404, "Team not found")

    if user.is_admin:
        return True

    if team.owner_id == user.id:
        return True

    raise HTTPException(403, "Not team admin")
