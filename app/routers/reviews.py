from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_buyer, get_current_admin_or_buyer
from app.db_depends import get_async_db
from app.models import Review as ReviewModel, Product as ProductModel, User as UserModel
from app.schemas import Review as ReviewSchema, ReviewCreate

router = APIRouter(prefix="/reviews", tags=["reviewes"])


@router.get("/", response_model=list[ReviewSchema])
async def get_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Получение списка всех отзывов.
    """
    request = await db.scalars(select(ReviewModel).where(ReviewModel.is_active.is_(True)))
    result = request.all()
    return result


async def update_product_results(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active.is_(True)
        )
    )
    avg_rating = result.scalar() or 0.0
    product = await db.get(ProductModel, product_id)
    product.rating = avg_rating
    await db.commit()


@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_buyer)
):
    """
    Создание отзыва для товара.
    """
    product_request = await db.scalars(select(ProductModel).where(
        ProductModel.is_active.is_(True),
        ProductModel.id == review.product_id
    ))
    product = product_request.first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    user_review_request = await db.scalars(select(ReviewModel).where(
        ReviewModel.is_active.is_(True),
        ReviewModel.product_id == product.id,
        ReviewModel.user_id == current_user.id
    ))
    user_review = user_review_request.first()
    if user_review is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user has already left a review for this product"
        )

    db_review = ReviewModel(**review.model_dump(), user_id=current_user.id)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    await update_product_results(db, review.product_id)
    return db_review


@router.delete("/{review_id}", status_code=status.HTTP_200_OK)
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_admin_or_buyer)
):
    """
    Удаление отзыва.
    """
    request = await db.scalars(select(ReviewModel).where(ReviewModel.id == review_id, ReviewModel.is_active.is_(True)))
    review = request.first()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    if review.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Current user is not the owner or admin")

    await db.execute(update(ReviewModel).where(ReviewModel.id == review_id).values(is_active=False))
    await db.commit()
    await db.refresh(review)
    await update_product_results(db, review.product_id)
    return {"message": "Review deleted"}

