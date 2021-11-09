from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from . import models as m
from .database import SessionLocal

def is_user(user_id: int) -> bool:
    with SessionLocal() as session:
        return session.query(m.User).filter(m.User.id == user_id).count() > 0

    
def add_user(user_id: int, username: str):
    with SessionLocal() as session:
        session.add(m.User(id=user_id, username=username))
        session.commit()


def change_user_tracking(user_id: int, tracking: bool):
    with SessionLocal() as session:
        user  = session.query(m.User).filter(m.User.id == user_id).first()
        user.tracking = tracking
        session.commit()


def change_user_studentid(user_id: int, studentid: str):
    with SessionLocal() as session:
        user = session.query(m.User).filter(m.User.id == user_id).first()
        user.studentid = studentid
        session.commit()