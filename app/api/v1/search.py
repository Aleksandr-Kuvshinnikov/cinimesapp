from fastapi import APIRouter, Query
from app.schemas.movies import MovieResponse, MovieSearchResponse

from app.services.tmdb import TMDBService

router= APIRouter(prefix='/search', tags=['Movies'])

@router.get('/', response_model=MovieSearchResponse)
async def search(name_of_movie:str= Query(description="Название фильма")):
    tmdbService = TMDBService()
    result= await tmdbService.search_movies(name_of_movie)
    return result



