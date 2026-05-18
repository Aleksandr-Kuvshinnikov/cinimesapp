from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError

from app.core.security import create_refresh_token
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.core.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User as UserModel
from app.core.security import hash_password, verify_password
from app.core.security import create_access_token
from app.schemas.user import RefreshTokenRequest, TokenResponse
from app.core.security import decode_access_token
router = APIRouter(prefix='/auth',tags=['auth'])


@router.post('/register', response_model=UserResponse)
async def register(user:UserCreate, db:AsyncSession= Depends(get_db)):
    """Регистрирует нового пользователя"""

    result= await db.scalar(select(UserModel).where(UserModel.email == user.email))
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    db_user = UserModel(username=user.username, email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.post('/login')
async def login(db:AsyncSession = Depends(get_db), user: OAuth2PasswordRequestForm = Depends()):
    user_db= await db.scalar(select(UserModel).where(UserModel.email == user.username))
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not(verify_password(user.password, user_db.hashed_password)):
        raise HTTPException(status_code=401, detail="Incorrect password")


    access_token= create_access_token(data={'sub' : str(user_db.id)})
    refresh_token= create_refresh_token(data= {'sub' : str(user_db.id)})
    return {'access_token': access_token, 'refresh_token' : refresh_token, 'token_type': 'bearer'}


@router.post('/refresh')
async def refresh_token(body:RefreshTokenRequest, db:AsyncSession = Depends(get_db)):
    old_refresh_token= body.refresh_token
    try:
        payload= decode_access_token(old_refresh_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Incorrect refresh token")

    if payload['token_type'] != 'refresh':
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id= payload.get('sub')
    access_token= create_access_token(data={'sub': str(user_id)})

    return {"access_token": access_token, "token_type": "bearer"}