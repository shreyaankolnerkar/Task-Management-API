from fastapi import HTTPException

from app.db.models import Team, User


def require_admin(user):
    if not user["is_admin"]:
        raise HTTPException(403, "Admin only")


def require_team_admin(team_id: int, user: User, db):
    team = db.get(Team, team_id)

    if not team:
        raise HTTPException(404, "Team not found")

    if user.is_admin:
        return True

    if team.owner_id == user.id:
        return True

    raise HTTPException(403, "Not team admin")
