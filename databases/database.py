from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#mysql connection url
db_url = "mysql+mysqlconnector://dextrus:Dextrus!1@10.10.20.29:3306/glossary_project"
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind = engine, autoflush=False, autocommit = False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()