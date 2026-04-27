import datetime
from .config import PG_DSN
from sqlalchemy import (
    DateTime,
    Integer,
    String,
    func,
    Text,
    Float,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedColumn, relationship
from .custom_types import ROLE

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):

    @property
    def id_dict(self):
        return {"id": self.id}


class User(Base):

    __tablename__ = "user"
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    name: MappedColumn[str] = mapped_column(String, unique=True)
    password: MappedColumn[str] = mapped_column(String)
    registration_time: MappedColumn[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    role: MappedColumn[ROLE] = mapped_column(String, default="user")
    advs: MappedColumn[list["Adv"]] = relationship(
        "Adv", lazy="selectin", back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "registration_time": self.registration_time,
        }


class Adv(Base):
    __tablename__ = "adv"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: MappedColumn["User"] = relationship("User", lazy="joined", back_populates="advs")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (UniqueConstraint("title", "user_id", name="unique_title_user"),)

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id,
        }


ORM_OBJ = User | Adv
ORM_CLS = type[User] | type[Adv]


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
