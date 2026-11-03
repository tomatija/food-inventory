
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends, status, HTTPException
from sqlmodel import Session, select


from database import (
    create_db_and_tables,
    get_session,
)
from models.item import Item, ItemCreate, ItemPublic, ItemUpdate


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


@app.get("/item/{item_id}", response_model=ItemPublic)
def get_item(session: SessionDep, item_id: int):
    item = session.get(Item, item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@app.patch("/items/{item_id}", response_model=ItemPublic)
def update_item(item_id: int, item: ItemUpdate, session: SessionDep):
    db_item = session.get(Item, item_id)

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.quantity = item.quantity

    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, session: SessionDep):
    db_item = session.get(Item, item_id)

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    session.delete(db_item)
    session.commit()
