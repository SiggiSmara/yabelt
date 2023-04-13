import enum
from typing import List, Optional
from sqlmodel import SQLModel, Field

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .database import Base


class MyState(enum.Enum):
    todo = 1
    doing = 2
    done = 3


class UserBase(SQLModel):
    email: str
    is_active: bool = True


class ItemTypeBase(SQLModel):
    title: str
    description: str = None


class ItemBase(SQLModel):
    title: str
    description: str = None
    owner: UserBase
    type: ItemTypeBase


class TaskBase(SQLModel):
    title: str
    description: str = None
    owner: UserBase
    state: MyState = MyState.todo
    needs_items: List[ItemTypeBase] = None


class ItemType(ItemTypeBase, table=True):
    id: int = Field(default=None, primary_key=True)


class Item(ItemBase, table=True):
    id: int = Field(default=None, primary_key=True)


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), index=True)
    description: Mapped[Optional[str]] = mapped_column(String(250), index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped[List["User"]] = relationship(back_populates="items")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), index=True)
    description: Mapped[Optional[str]] = mapped_column(String(250), index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    state: Mapped[MyState] = mapped_column(
        Enum(MyState), default=MyState.todo, index=True
    )

    owner: Mapped[List["User"]] = relationship(back_populates="tasks")
