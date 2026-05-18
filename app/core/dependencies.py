from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
from collections.abc import AsyncGenerator
from app.core.security import decode_access_token
from jose import JWTError
from app.models.user import User as UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login") #

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Создает асинхронное соеденение с PostgreSQL"""
    async with async_session() as session:
        yield session

async def get_current_user(db:AsyncSession= Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        user_id = payload.get('sub')
        if user_id is None:
            raise HTTPException(status_code=401, detail="Невалидный токен")

    except JWTError:
        raise HTTPException(status_code=401, detail="Невалидный токен")

    result= await db.scalars(select(UserModel).where(UserModel.id == int(user_id), UserModel.is_active == True))
    user= result.first()
    if user is None:
        raise HTTPException(status_code=401)
    return user


