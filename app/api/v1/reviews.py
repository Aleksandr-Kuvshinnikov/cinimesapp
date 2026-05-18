from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_current_user
from app.core.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User as UserModel
from app.models.review import Review as ReviewModel
from sqlalchemy import select, update
from app.schemas.reviews import ReviewCreate, ReviewResponse



router= APIRouter(prefix="/movies", tags=["reviews"])

@router.post("/{movie_id}/reviews", response_model=ReviewResponse)
async def add_review(movie_id: int, review: ReviewCreate, db:AsyncSession= Depends(get_db), user: UserModel = Depends(get_current_user)):
    """Добавление отзыва к фильму(пользовательможет оставить только один комментрий к фильму!!!)"""
    result= await db.scalar(select(ReviewModel).where(ReviewModel.movie_id == movie_id, ReviewModel.user_id == user.id, ReviewModel.is_active == True))
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A user can leave only one comment on one film.")
    db_review = ReviewModel(**review.model_dump(), user_id = user.id, movie_id = movie_id)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review


@router.get('/{movie_id}/reviews', response_model=list[ReviewResponse])
async def get_reviews(movie_id:int, db:AsyncSession= Depends(get_db), user:UserModel= Depends(get_current_user)):
    result= await db.scalars(select(ReviewModel).where(ReviewModel.movie_id == movie_id, ReviewModel.is_active == True))
    db_reviews = result.all()
    if db_reviews is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The movie don't have reviews")

    return db_reviews


@router.delete('/{movie_id}/reviews/{review_id}', response_model=ReviewResponse)
async def delete_review(movie_id:int, review_id:int, db:AsyncSession = Depends(get_db), user:UserModel= Depends(get_current_user)):
    result= await db.scalar(select(ReviewModel).where(ReviewModel.movie_id == movie_id, ReviewModel.id == review_id, ReviewModel.is_active == True, ReviewModel.user_id == user.id))
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The movie don't have reviews")

    await db.execute(update(ReviewModel).where(ReviewModel.movie_id == movie_id, ReviewModel.id == review_id, ReviewModel.user_id == user.id).values(is_active = False))

    await db.commit()
    await db.refresh(result)
    return result


