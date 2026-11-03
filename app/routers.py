
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


# CREATE USER
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    user = User(
        name=data.name,
        email=data.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# GET ALL USERS
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):

    return db.query(User).all()


# GET USER BY ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# UPDATE USER
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if data.name is not None:
        user.name = data.name

    if data.email is not None:

        existing = db.query(User).filter(
            User.email == data.email,
            User.id != user_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

        user.email = data.email

    db.commit()
    db.refresh(user)

    return user


# DELETE USER
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
