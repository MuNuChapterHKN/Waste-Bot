from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


SQLALCHEMY_DATABASE_URL =  os.environ.get('DATABASE_URL')
echo = os.environ.get('DATABASE_LOGGING') == 'True'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo = echo,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()