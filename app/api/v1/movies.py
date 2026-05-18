from fastapi import APIRouter
from app.services.tmdb import TMDBService
from app.schemas.movies import MovieSearchResponse, MovieResponse
router = APIRouter(prefix='/movies', tags=['Movies'])

tmdb= TMDBService()


@router.get('/popular', response_model=MovieSearchResponse)
async def popular():
    result = await tmdb.get_popular_movies()
    return result


@router.get('/{movie_id}')
async def get_movie_by_id(movie_id:int) -> MovieResponse:
    result= await tmdb.get_movie_details(movie_id)
    return result