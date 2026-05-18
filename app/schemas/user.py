from pydantic import BaseModel, EmailStr



class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str


class UserLogin(BaseModel):
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr
    is_active:bool
    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str