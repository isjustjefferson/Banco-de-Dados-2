# database/connection.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config.settings import DB_URL  


engine = create_engine(DB_URL, echo=False)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

session = scoped_session(SessionLocal)