from jose import jwt
from datetime import datetime, timedelta, UTC
# import os
# from dotenv import load_dotenv

users = [
    {"id":1, "name":"Rakhi", "username":"Rakhi123","password":"secret1"},
    {"id":2, "name":"Shivam", "username":"Shivam123","password":"secret2"},
    {"id":3, "name":"Chetna", "username":"Chetna123","password":"secret3"}
]
# setting up jwt manually
secret_key = 'mysecret'
Algorithm = 'HS256'
token_expiry = 20

# creating token
def create_token(username: str):
    expire = datetime.now(UTC) + timedelta(minutes = token_expiry)
    payload = {"sub":username, "exp":expire}
    return jwt.encode(payload, secret_key, algorithm = Algorithm)

# verifying user
def verify_user(username : str, password: str):
    for user in users:
        if user['username'] == username and user['password'] == password:
            return True
    return False


