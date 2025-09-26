from fastapi import FastAPI
from routers import users,glossaries
from models import model
from databases.database import engine

model.Base.metadata.create_all(bind =engine)
app = FastAPI()
app.include_router(users.router)

app.include_router(glossaries.router)