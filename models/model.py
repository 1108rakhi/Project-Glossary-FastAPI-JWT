from sqlalchemy import Column, Integer, String, DateTime
from databases.database import Base
from sqlalchemy.sql import func
from datetime import datetime, UTC
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60))
    username = Column(String(60), unique=True)
    password = Column(String(60))
    role = Column(String(10), default='user')

class Glossary(Base):
    __tablename__ = 'glossary'
    id = Column(Integer, primary_key=True, index=True)
    term = Column(String(20), nullable=False)
    description = Column(String(255))
    created_by = Column(String(50))
    updated_by = Column(String(50))
    created_at = Column(DateTime(timezone=True),default=datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(UTC))
