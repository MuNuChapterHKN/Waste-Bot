from sqlalchemy.sql.sqltypes import Boolean
from .database import Base

from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    tracking = Column(Boolean, default=False, nullable=False)

    studentid = Column(String(7), nullable=True)
