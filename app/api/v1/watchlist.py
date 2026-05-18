from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.core.dependencies import get_db
from app.models.user import User as UserModel
from app.models.watchlist import WatchList as WatchListModel
from sqlalchemy import select, update
from app.schemas.watchlist import WatchlistResponse, WatchlistCreate, WatchlistUpdate


router= APIRouter(prefix="/watchlist", tags=["watchlist"])

@router.get("/", response_model=list[WatchlistResponse])
async def my_watchlist(db:AsyncSession = Depends(get_db), user:UserModel= Depends(get_current_user)):
    """Показывает все фильмы из списка пользователя"""
    watchlist= await db.scalars(select(WatchListModel).where(WatchListModel.user_id == user.id))
    db_watchlist= watchlist.all()
    if db_watchlist is None:
        raise HTTPException(status_code=404, detail="User don't have watchlist")

    return db_watchlist



@router.post('/', response_model= WatchlistResponse)
async def add_movie_in_watchlist(watchlist:WatchlistCreate,
                                 db:AsyncSession= Depends(get_db),
                                 user:UserModel= Depends(get_current_user),
                                 ):

    """Добовляет в муви лист новый фильм"""
    db_movie = WatchListModel(**watchlist.model_dump(), user_id= user.id)
    db.add(db_movie)
    await db.commit()
    await db.refresh(db_movie)
    return db_movie


@router.put('/{watchlist_id}', response_model=WatchlistResponse)
async def update_watchlist(
        watchlist_id:int,
        watchlist:WatchlistUpdate,
        db:AsyncSession= Depends(get_db),
        user:UserModel= Depends(get_current_user),):

    res= await db.scalar(select(WatchListModel).where(WatchListModel.id == watchlist_id, WatchListModel.user_id == user.id, WatchListModel.is_active == True))

    if res is None:
        raise HTTPException(status_code=404, detail="User don't have watchlist")

    await db.execute(update(WatchListModel).where(WatchListModel.user_id == user.id, WatchListModel.id == watchlist_id).values(**watchlist.model_dump()))
    await db.commit()
    await db.refresh(res)
    return res

@router.delete('/{watchlist_id}', response_model=WatchlistResponse)
async def delete(watchlist_id:int, db:AsyncSession= Depends(get_db), user:UserModel= Depends(get_current_user)):
    res= await db.scalar(select(WatchListModel).where(WatchListModel.id == watchlist_id, WatchListModel.is_active == True, WatchListModel.user_id == user.id))

    if res is None:
        raise HTTPException(status_code=404, detail="User don't have watchlist")

    await db.execute(update(WatchListModel).where(WatchListModel.id == watchlist_id).values(is_active=False))
    await db.commit()
    await db.refresh(res)
    return res
