from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60))
    username = Column(String(60), unique=True)
    password = Column(String(60))
    role = Column(String(10), default='user')