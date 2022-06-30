from . import models as m
from .database import SessionLocal


def is_user(user_id: int) -> bool:
    with SessionLocal() as session:
        return session.query(m.User).filter(m.User.id == user_id).count() > 0


def add_user(user_id: int):
    with SessionLocal() as session:
        session.add(m.User(id=user_id))
        session.commit()


def user_enable_tracking(user_id: int):
    with SessionLocal() as session:
        user = session.query(m.User).filter(m.User.id == user_id).first()
        user.tracking = True
        session.commit()


def user_disable_tracking(user_id: int):
    with SessionLocal() as session:
        user = session.query(m.User).filter(m.User.id == user_id).first()
        user.tracking = False
        session.commit()