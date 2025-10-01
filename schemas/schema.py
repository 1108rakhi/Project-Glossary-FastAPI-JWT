from pydantic import BaseModel
from datetime import datetime
from typing import Optional

#user login
class LoginRequest(BaseModel):
    username : str
    password : str

#user signup
class CreateUser(BaseModel):
    name : str
    username : str
    password : str
    role : str='user'

#user get response
class UserResponse(BaseModel):
    # id : int
    name : str
    username : str
    role : str

    class Config:
        orm_mode = True

# glossary creation
class CreateGlossary(BaseModel):
    term :str
    description : str

class UpdateGlossary(BaseModel):
    term: Optional[str] = None
    description : Optional[str] = None

#glossary response
class GlossaryResponse(BaseModel):
    id : int
    term:str
    description : str
    created_by : Optional[str] = None
    updated_by : Optional[str]=None
    created_at: Optional[datetime] = None
    updated_at : Optional[datetime] = None
    class Config:
        orm_mode = True

class GlossaryPagination(BaseModel):
    term: str
    description : str
    class Config:
        orm_mode = True