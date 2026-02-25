# Синхронное подключение к sqlite
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///test_project.db"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)


# Асинхронное подключение к postresql
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://test_user:123456@localhost:5432/test_db"
async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


# ----------------------------------------------------------------------
# from sqlalchemy import Column, Integer, String, Float, Table
# from sqlalchemy.orm import registry, mapped_column, Mapped
# from datetime import datetime
#
#
# ----------------------------------------------------------------------
# class Product(Base):
#     __tablename__ = "products"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
#     sku: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
#     name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
#     description: Mapped[str] = mapped_column(String(500), default="")
#     price: Mapped[float] = mapped_column(nullable=False)
#     is_available: Mapped[bool] = mapped_column(default=False)
#     created_at: Mapped[datetime] = mapped_column(default=datetime.now)
#
#
# ----------------------------------------------------------------------
# class Product(Base):
#     __tablename__ = "products"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     description = Column(String)
#     price = Column(Float, nullable=False)
#
#
# ----------------------------------------------------------------------
# mapper_registry = registry()
# metadata = mapper_registry.metadata
#
#
# product_table = Table(
#     "products",
#     metadata,
#     Column("id", Integer, primary_key=True, index=True),
#     Column("name", String, nullable=False),
#     Column("description", String),
#     Column("price", Float, nullable=False)
# )
#
# metadata.create_all(engine)
# ----------------------------------------------------------------------
