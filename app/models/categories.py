from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")
    parent: Mapped["Category | None"] = relationship("Category", back_populates="children", remote_side="Category.id")
    children: Mapped[list["Category"]] = relationship("Category", back_populates="parent")


# --------------------------------------------------------------------------------
# from decimal import Decimal
# from datetime import date, datetime
#
# from sqlalchemy import String, Boolean, Numeric, Date, DateTime, Text
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
#
#
# class Base(DeclarativeBase):
#     pass
#
#
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# class Recipe(Base):
#     __tablename__ = "recipes"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(150), nullable=False)
#     cooking_time: Mapped[int] = mapped_column(nullable=False)
#     ingredients: Mapped[str] = mapped_column(Text, nullable=False)
#     calories: Mapped[int]
#     created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
#
#
# --------------------------------------------------------------------------------
# class Car(Base):
#     __tablename__ = "cars"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     brand: Mapped[str] = mapped_column(String(50), nullable=False)
#     model: Mapped[str] = mapped_column(String(50), nullable=False)
#     year: Mapped[int] = mapped_column(nullable=False)
#     price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
#     is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
#
#
# # --------------------------------------------------------------------------------
# class Event(Base):
#     __tablename__ = "events"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str] = mapped_column(String(100), nullable=False)
#     start_time: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
#     end_time: Mapped[datetime | None] = mapped_column(DateTime())
#     description: Mapped[str | None] = mapped_column(Text())
#
#
# --------------------------------------------------------------------------------
# class Movie(Base):
#     __tablename__ = "movies"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str] = mapped_column(String(200), nullable=False)
#     duration: Mapped[int] = mapped_column(nullable=False)
#     release_date: Mapped[date | None] = mapped_column(Date(), nullable=True)
#
#
# --------------------------------------------------------------------------------
# class Product(Base):
#     __tablename__ = "products"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(150), nullable=False)
#     price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
#     stock_quantity: Mapped[int] = mapped_column(nullable=False, default=0)
#
#
# --------------------------------------------------------------------------------
# class Task(Base):
#     __tablename__ = "tasks"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str] = mapped_column(String(100), nullable=False)
#     is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
#
#
# --------------------------------------------------------------------------------
# class Category(Base):
#     __tablename__ = "categories"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(50), nullable=False)
# --------------------------------------------------------------------------------


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable
    from app.models.products import Product

    print(CreateTable(Category.__table__))
    print(CreateTable(Product.__table__))

