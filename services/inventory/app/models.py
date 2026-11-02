
from sqlmodel import SQLModel, Field


class ItemBase(SQLModel):
    name: str
    quantity: int = Field(default=1, ge=0)


class Item(ItemBase, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True
    )


class ItemCreate(ItemBase):
    pass


class ItemPublic(ItemBase):
    id: int
