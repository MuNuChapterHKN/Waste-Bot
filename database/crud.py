from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from . import models as m
from .database import SessionLocal

def is_user(user_id: int) -> bool:
    with SessionLocal() as session:
        return session.query(m.User).filter(m.User.id == user_id).count() > 0

    
def change_user_studentid(user_id: int, studentid: str):
    with SessionLocal() as session:
        user = session.query(m.User).filter(m.User.id == user_id).first()
        user.studentid = studentid
        session.commit()


def user_enable_tracking(user_id: int, studentid: str):
    with SessionLocal() as session:
        user = session.query(m.User).filter(m.User.id == user_id).first()
        user.tracking = True
        user.studentid = studentid
        session.commit()


def user_disable_tracking(user_id: int):
    with SessionLocal() as session:
        user = session.query(m.User).filter(m.User.id == user_id).first()
        user.tracking = False
        user.username = None
        session.commit()