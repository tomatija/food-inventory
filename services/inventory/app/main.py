
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends, status
from sqlmodel import Session, select

from database import (
    create_db_and_tables,
    get_session,
)
from models import Item, ItemCreate, ItemPublic


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

SessionDep = Annotated[Session, Depends(get_session)]


@app.post(
    "/items",
    response_model=ItemPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_item(item: ItemCreate, session: SessionDep):
    db_item = Item.model_validate(item)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item


@app.get("/items", response_model=list[ItemPublic])
def get_items(session: SessionDep):
    return session.exec(select(Item)).all()
