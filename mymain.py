from fastapi import FastAPI
from myapp.routers import users
from myapp.models import model
from myapp.databases.database import engine

model.Base.metadata.create_all(bind =engine)
app = FastAPI()
app.include_router(users.router)

