from datetime import date, datetime, timezone
from decimal import Decimal
from sqlmodel import SQLModel, Field
from enum import Enum

class Unit(str, Enum):
    PCS = "pcs"
    G = "g"
    KG = "kg"
    ML = "ml"
    L = "l"

class ItemBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    category: str | None = None
    quantity: Decimal = Field(default=Decimal("1"), ge=0)
    unit: Unit
    expiration_date: date | None = None
    product_id: int | None = None


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ItemCreate(ItemBase):
    pass


class ItemPublic(ItemBase):
    id: int

class ItemUpdate(SQLModel):
    quantity: Decimal = Field(ge=0)
