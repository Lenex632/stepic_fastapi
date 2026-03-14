from decimal import Decimal

from sqlalchemy import String, Boolean, Integer, Numeric, ForeignKey, text, Computed, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TSVECTOR

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(200), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    raiting: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0.0, server_default=text("0"))

    tsv: Mapped[TSVECTOR] = mapped_column(
        TSVECTOR,
        Computed(
            """
            setweight(to_tsvector('english', coalesce(name, '')), 'A')
            ||
            setweight(to_tsvector('english', coalesce(description, '')), 'B')
            """,
            persisted=True
        ),
        nullable=False
    )

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    seller: Mapped["User"] = relationship("User", back_populates="products")

    __table_args__ = Index("ix_products_tsv_gin", "tsv", postgresql_using="gin"),


# -------------------------------------------------------------------------------------
# from sqlalchemy import String, ForeignKey, Text, Numeric
# from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
#
# from decimal import Decimal
#
#
# class Base(DeclarativeBase):
#     pass
#
#
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# class Customer(Base):
#     __tablename__ = "customers"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(100), nullable=False)
#     email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
#
#     orders: Mapped[list["Order"]] = relationship("Order", back_populates="customer")
#
#
# class Order(Base):
#     __tablename__ = "orders"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     order_number: Mapped[int] = mapped_column(String(20), unique=True, nullable=False)
#     total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
#     customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
#
#     customer: Mapped["Customer"] = relationship("Customer", back_populates="orders")
#
#
# -------------------------------------------------------------------------------------
# class Category(Base):
#     __tablename__ = "categories"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(50), nullable=False)
#
#     products: Mapped[list["Product"]] = relationship("Product", back_populates="category")
#
#
# class Product(Base):
#     __tablename__ = "products"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(150), nullable=False)
#     price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
#     category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
#
#     category: Mapped["Category"] = relationship("Category", back_populates="products")
#
#
# -------------------------------------------------------------------------------------
# class User(Base):
#     __tablename__ = "users"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
#
#     profile: Mapped["Profile"] = relationship("Profile", uselist=False, back_populates="user")
#
#
# class Profile(Base):
#     __tablename__ = "profiles"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
#     bio: Mapped[str | None] = mapped_column(Text)
#
#     user: Mapped["User"] = relationship("User", uselist=False, back_populates="profile")
#
#
# -------------------------------------------------------------------------------------
# class Author(Base):
#     __tablename__ = "authors"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(100), nullable=False)
#
#     book: Mapped[list["Book"]] = relationship("Book", back_populates="author")
#
#
# class Book(Base):
#     __tablename__ = "books"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str] = mapped_column(String(200), nullable=False)
#     author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), unique=True, nullable=False)
#
#     author: Mapped["Author"] = relationship("Author", back_populates="book")
# -------------------------------------------------------------------------------------

