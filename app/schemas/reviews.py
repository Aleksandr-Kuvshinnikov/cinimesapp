from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    text:str
    rating: int = Field(..., ge=1, le= 10)

class ReviewResponse(BaseModel):
    id: int
    movie_id: int
    text: str
    rating: int
    user_id: int
    model_config = {"from_attributes": True}