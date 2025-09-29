from fastapi import FastAPI
from router_users import users
from router_glossary import glossaries
from models import model
from databases.database import engine

model.Base.metadata.create_all(bind =engine)
app = FastAPI()
app.include_router(users.router)

app.include_router(glossaries.router)