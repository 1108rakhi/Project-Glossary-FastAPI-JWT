from jose import jwt
from datetime import datetime, timedelta, UTC
from sqlalchemy.orm import Session
from . import models, database, schemas
from fastapi import APIRouter, Depends, HTTPException

# setting up jwt manually
secret_key = 'mysecret'
Algorithm = 'HS256'
token_expiry = 20

router = APIRouter()

# creating token
def create_token(data:dict, expires_delta:timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, secret_key, algorithm = Algorithm)

# verifying user
@router.post('/login')
def login(request: schemas.LoginRequest, db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail = 'Invalid username or password')
    
    access_token = create_token(data = {"sub":user.username})
    return {'access_token' : access_token, 'token_type': "bearer"}


