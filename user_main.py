from fastapi import FastAPI
from . import users, models, database

models.Base.metadata.create_all(bind = database.engine)
app = FastAPI()
app.include_router(users.router)

