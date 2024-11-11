from typing import Any

from sqlmodel import Session, select

from models import User, UserCreate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    # try:
    db_obj = User.model_validate(user_create)
    print("no bug before model validate")
    session.add(db_obj)
    print("no bug before db add")
    session.commit()
    print("no bug before db commit")
    session.refresh(db_obj)
    # except Exception as e:
    #     print(f'err in here {e}')
    #     session.rollback()
    return db_obj


def get_all_users(*, session: Session) -> list[User]:
    # 屏蔽掉 root, 只对用户展示他们平级的
    statement = select(User).where(User.full_name != "root")
    return session.exec(statement).all()


def get_user_by_full_name(*, session: Session, full_name: str) -> User | None:
    statement = select(User).where(User.full_name == full_name)
    session_user = session.exec(statement).first()
    return session_user

def get_user_by_port(*, session: Session, port: str) -> User | None:
    statement = select(User).where(User.port == port)
    session_user = session.exec(statement).first()
    return session_user


def del_user_by_full_name(*, session: Session, full_name: str) -> None:
    pass
