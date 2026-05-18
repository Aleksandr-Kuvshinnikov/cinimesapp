from pydantic import BaseModel, Field


class WatchlistCreate(BaseModel):
    """Для добовления фильмов"""
    movie_id: int
    status: str = Field(..., pattern='^(want|watching|watched)$')



class WatchlistUpdate(BaseModel):
    status: str = Field(..., pattern='^(want|watching|watched)$')

class WatchlistResponse(BaseModel):
    id:int
    movie_id: int
    status: str
    user_id: int
    model_config = {"from_attributes": True}