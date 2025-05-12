from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    surname: Optional[str] = None
    age: Optional[int] = None
class UserUpdate(SQLModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    age: Optional[int] = None