from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Path
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import List, Optional 

# Define the model
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    surname: Optional[str] = None
    age: Optional[int] = None
# Model for partial updates (all fields optional)
class UserUpdate(SQLModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    age: Optional[int] = None

# Database config  
dbname = "learnFastAPI"
DATABASE_URL = f"postgresql+psycopg2://postgres:password@localhost/{dbname}"
engine = create_engine(DATABASE_URL, echo=True)

# Create table on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

# Initialize app with lifespan
app = FastAPI(lifespan=lifespan)

# POST endpoint to add user
@app.post("/users/")
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

# GET endpoint to read users
@app.get("/users/", response_model=List[User])  # Add response_model
def read_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users
# GET endpoint to read a single user by ID
@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
      
    # DELETE endpoint to remove a user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"message": f"User with ID {user_id} deleted successfully"}
    

# PUT endpoint to update a user
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: UserUpdate):
    with Session(engine) as session:
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