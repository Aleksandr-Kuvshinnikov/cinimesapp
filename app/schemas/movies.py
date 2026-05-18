

from pydantic import BaseModel

class MovieResponse(BaseModel):
    id:int
    title:str
    overview:str
    release_date:str|None = None
    vote_average:float|None = None
    poster_path:str|None


class MovieSearchResponse(BaseModel):
    results:list[MovieResponse]
    total_results:int
    total_pages:int
