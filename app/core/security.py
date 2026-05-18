from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from .config import settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30


ALGORITHM = "HS256"
def hash_password(password:str)-> str:
    """Преобразует пароль в хеш"""
    return pwd_context.hash(password)

def verify_password(password:str, hashed_password:str) -> bool:
    """Проверяет совпадают ли пароли"""
    return pwd_context.verify(password, hashed_password)



def create_access_token(data:dict) -> str:
    """Создает JWT с payload (sub, exp)"""
    to_encode= data.copy()
    expire= datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire, "token_type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data:dict) -> str:
    """Создает refresh-token с длительным сроком действия и token-type= refresh"""

    to_encode= data.copy()
    expire= datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp":expire, "token_type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)




def decode_access_token(token:str) -> dict:
    payload= jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    return payload


