from pydantic import BaseModel

#login
class LoginRequest(BaseModel):
    username : str
    password : str

#signup
class CreateUser(BaseModel):
    name : str
    username : str
    password : str
    role : str='user'

#get response
class UserResponse(BaseModel):
    id : int
    name : str
    username : str
    role : str

    class Config:
        orm_mode = True