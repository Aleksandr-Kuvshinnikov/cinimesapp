from pydantic import BaseModel


class LikeResponse(BaseModel):
    id:int
    movie_id: int
    user_id:int


