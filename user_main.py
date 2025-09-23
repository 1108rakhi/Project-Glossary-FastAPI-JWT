from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from myapp import users

app = FastAPI()

@app.post('/login')
def login(form_data : OAuth2PasswordRequestForm = Depends()):
    if not users.verify_user(form_data.username, form_data.password):
        raise HTTPException(status_code= 401, detail='Invalid Credentials, Please try again')
    token = users.create_token(form_data.username)
    return {
        "access_token" : token,
        'token_type' : "bearer"
    }