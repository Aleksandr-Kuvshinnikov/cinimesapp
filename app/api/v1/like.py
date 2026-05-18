from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_current_user
from app.core.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User as UserModel
from app.schemas.like import LikeResponse
from sqlalchemy import select, update, func
from app.models.like import Like as LikeModel


router = APIRouter(prefix="/movies", tags=["like"])



@router.post("/{movie_id}/like", response_model=LikeResponse)
async def add_like(movie_id:int, user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    res= await db.scalar(select(LikeModel).where(LikeModel.movie_id == movie_id, LikeModel.user_id == user.id, LikeModel.is_active == True))
    if res:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already liked this movie")

    db_like = LikeModel(movie_id=movie_id, user_id=user.id)
    db.add(db_like)
    await db.commit()
    await db.refresh(db_like)
    return db_like

@router.delete('/{movie_id}/like', response_model=LikeResponse)
async def delete_like(movie_id:int, user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res = await db.scalar(select(LikeModel).where(LikeModel.movie_id == movie_id, LikeModel.user_id == user.id,
                                                  LikeModel.is_active == True))
    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User don't like this movie")

    await db.execute(update(LikeModel).where(LikeModel.movie_id == movie_id, LikeModel.user_id == user.id).values(is_active=False))
    await db.commit()
    await db.refresh(res)
    return res


@router.get('/{movie_id}/likes')
async def count_of_likes(movie_id:int, db: AsyncSession = Depends(get_db)):
    count= await db.scalar(select(func.count()).where(LikeModel.movie_id == movie_id, LikeModel.is_active == True))

    return {'movie_id':movie_id, 'likes_count':count}


