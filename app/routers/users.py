from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from ..models import User, UserUpdate
from ..database import get_session

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/", response_model=List[User])
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


    # DELETE endpoint to remove a user
@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"message": f"User with ID {user_id} deleted successfully"}
    

# PUT endpoint to update a user
@router.put("/{user_id}", response_model=User)
def update_user(user_id: int,updated_user: UserUpdate, session: Session = Depends(get_session)):
  
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = updated_user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


# @app.get("/users/{user_id}", response_model=User)
# def read_user(user_id: int):
#     with Session(engine) as session:
#         user = session.get(User, user_id)
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         return user
# # POST endpoint to add user
# @app.post("/users/")
# def create_user(user: User):
#     with Session(engine) as session:
#         session.add(user)
#         session.commit()
#         session.refresh(user)
#         return user

# # GET endpoint to read users
# @app.get("/users/", response_model=List[User])  # Add response_model
# def read_users():
#     with Session(engine) as session:
#         users = session.exec(select(User)).all()
#         return users
# # GET endpoint to read a single user by ID

      
#     # DELETE endpoint to remove a user
# @app.delete("/users/{user_id}")
# def delete_user(user_id: int):
#     with Session(engine) as session:
#         user = session.get(User, user_id)
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         session.delete(user)
#         session.commit()
#         return {"message": f"User with ID {user_id} deleted successfully"}
    

# # PUT endpoint to update a user
# @app.put("/users/{user_id}", response_model=User)
# def update_user(user_id: int, updated_user: UserUpdate):
#     with Session(engine) as session:
#         user = session.get(User, user_id)
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         user_data = updated_user.dict(exclude_unset=True)
#         for key, value in user_data.items():
#             setattr(user, key, value)
#         session.add(user)
#         session.commit()
#         session.refresh(user)
#         return user