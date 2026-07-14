import httpx
from app.core.config import settings
class TMDBService:
    BASE_URL= 'https://api.themoviedb.org/3'

    async def get_popular_movies(self):
        async with httpx.AsyncClient() as client:
            response= await client.get(self.BASE_URL + '/movie/popular', params= {"api_key": settings.TMDB_API_KEY, "language": "ru-Ru"})
            return response.json()


    async def search_movies(self, query:str):
        async with httpx.AsyncClient() as client:
            response= await client.get(self.BASE_URL + '/search/movie', params= {"query": query, 'api_key': settings.TMDB_API_KEY, 'language': 'ru-Ru'})
            return response.json()



    async def get_movie_details(self, movie_id: int):
        async with httpx.AsyncClient() as client:
            response= await client.get(self.BASE_URL + f'/movie/{movie_id}', params={"api_key": settings.TMDB_API_KEY, "language": "ru-Ru"})
            return response.json()



