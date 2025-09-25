from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC
from sqlalchemy.orm import Session
from myapp.models import model
from myapp.databases import database
from myapp.schemas import schema
from fastapi import APIRouter, Depends, HTTPException, Query, Header

# setting up jwt manually
secret_key = 'mysecret'
Algorithm = 'HS256'
token_expiry = 5

router = APIRouter()

# creating token
def create_token(data:dict, expire_time:timedelta = timedelta(minutes=token_expiry)):
    to_encode = data.copy()
    expire = datetime.now(UTC) + expire_time
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, secret_key, algorithm = Algorithm)

def decode_token(token: str):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=[Algorithm])
        return decoded
    except JWTError:
        raise HTTPException(status_code=401, detail = 'Invalid token')
    

# checking role
def check_role(authorization : str , role_access: str = 'admin'):
    if not authorization:
        raise HTTPException(status_code=401, detail='Invalid authorization')
    
    role_check = decode_token(authorization)
    role = role_check.get('role')
    if role != role_access:
        raise HTTPException(status_code=403, detail='Access denied')
    return role_check

#signup
@router.post('/signup', response_model=schema.UserResponse)
def signup(user_request : schema.CreateUser, db:Session = Depends(database.get_db), checkrole:dict = Depends(check_role)):
    existing_user = db.query(model.User).filter(model.User.username == user_request.username).first()
    if existing_user:
        raise HTTPException(status_code=401, detail = 'Username already exists')
    
    new_user = model.User(
        name = user_request.name,
        username = user_request.username,
        password = user_request.password,
        role = user_request.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# login
@router.post('/login')
def login(request: schema.LoginRequest, db:Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.username == request.username).first()
    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail = 'Invalid username or password')
    
    access_token = create_token(data = {"sub":user.username, 'role':user.role})
    return {'access_token' : access_token, 'token_type': "bearer"}


@router.get("/users", response_model=list[schema.UserResponse])
def get_users(name : str | None = Query(None), db : Session = Depends(database.get_db)):
    query = db.query(model.User)
    if name:
        query = query.filter(model.User.name == name)
    users = query.all()
    return users

@router.put('/users/{id}', response_model=schema.UserResponse)
def update_user(id: int, update:schema.CreateUser, db:Session = Depends(database.get_db),checkrole:dict = Depends(check_role)):
    upd_user = db.query(model.User).filter(model.User.id == id).first()
    if not upd_user:
        raise HTTPException(status_code=404, detail='User not found')
    upd_user.name = update.name
    upd_user.username = update.username
    upd_user.password = update.password
    upd_user.role = update.role
    db.commit()
    db.refresh(upd_user)
    return upd_user

@router.delete('/users/{id}')
def delete_user(id: int, db: Session = Depends(database.get_db),checkrole:dict = Depends(check_role)):
    del_user = db.query(model.User).filter(model.User.id == id).first()
    if not del_user:
        raise HTTPException(status_code= 404, detail='User not found')
    db.delete(del_user)
    db.commit()
    return {'message':'User deleted successfully'}
