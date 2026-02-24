# ----------------------------------------------------------------
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter()

# ----------------------------------------------------------------
from app.models.post import PostModel


@router.delete("/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    stmt = select(PostModel).where(PostModel.id == post_id, PostModel.is_active.is_(True))
    post = db.scalars(stmt).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.execute(update(PostModel).where(PostModel.id == post_id).values(is_active=False))
    db.commit()

    return "Post marked as inactive"


# ----------------------------------------------------------------
from app.models.review import ReviewModel
from app.models.product import ProductModel
from app.schemas.review import ReviewSchema, ReviewCreate


@router.put("/{review_id}", response_model=ReviewSchema)
async def update_product(review_id: int, review: ReviewCreate, db: Session = Depends(get_db)):
    stmt = select(ReviewModel).where(ReviewModel.id == review_id, ReviewModel.is_active.is_(True))
    db_review = db.scalars(stmt).first()
    if db_review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    product_stmt = select(ProductModel).where(ProductModel.id == db_review.product_id, ProductModel.is_active.is_(True))
    product = db.scalars(product_stmt).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.execute(
        update(ReviewModel)
        .where(ReviewModel.id == review_id)
        .values(**review.model_dump())
    )
    db.commit()
    db.refresh(db_review)
    return db_review


# ----------------------------------------------------------------
from app.models.order import OrderModel
from app.models.user import UserModel
from app.schemas.order import OrderSchema


@router.get("/{order_id}", response_model=OrderSchema)
async def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    stmt = select(OrderModel).where(OrderModel.id == order_id, OrderModel.is_active.is_(True))
    order = db.scalars(stmt).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user_stmt = select(UserModel).where(UserModel.id == order.user_id, UserModel.is_active.is_(True))
    user = db.scalars(user_stmt).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return order


# ----------------------------------------------------------------
from app.models.category import CategoryModel
from app.schemas.category import CategorySchema, CategoryCreate


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# ----------------------------------------------------------------
from app.models.user import UserModel
from app.schemas.user import UserSchema


@router.get("/", response_model=list[UserSchema])
async def get_users(db: Session = Depends(get_db)):
    stmt = select(UserModel).where(UserModel.is_active.is_(True))
    users = db.scalars(stmt).all()

    return users
# ----------------------------------------------------------------

