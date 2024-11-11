from collections.abc import Generator
from typing import Annotated
from sqlmodel import SQLModel, Session, create_engine, select
from fastapi import Depends
from models import User, UserCreate
import crud


engine = create_engine("sqlite:///tutorial.db", connect_args={"check_same_thread": False})




# backend per start
SQLModel.metadata.create_all(engine)

session = Session(engine)
# 此时还没有数据
# 嗯, 奇怪, 加上下面这些就行, 不加就不行, 再尝试一下    
user = session.exec(
    select(User).where(User.full_name == "root")
).first()
print("no bug before query")
if user:
    print("exist user is:", user)
if not user:
    user_in = UserCreate(
        full_name="root",
        port=8000,
    )
    print(user_in)
    print("no bug here")
    user = crud.create_user(session=session, user_create=user_in)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]
