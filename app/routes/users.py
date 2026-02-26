from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.authentication.auth import (create_token, hash_password,
                                     verify_password)
from app.authentication.dependencies import get_current_user
from app.db.models import User
from app.db.schemas import UserCreate, UserLogin, UserOut
from app.db.session import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == user.email).first()
    if exists:
        raise HTTPException(400, "Email already exists")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        is_admin=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User created"}


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"user_id": user.id})
    return {"access_token": token}


@router.get("/profile", response_model=UserOut)
def profile(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "is_admin": current_user.is_admin,
        "message": "User Authenticated",
    }


@router.put("/users/{user_id}/make-admin")
def make_admin(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    user.is_admin = True
    db.commit()
    return {"msg": "User promoted to admin"}
