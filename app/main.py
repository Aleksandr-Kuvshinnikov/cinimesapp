from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.api.v1.search import router as search_router
from app.api.v1.movies import router as movie_router
from app.api.v1.watchlist import router as watchlist_router
from app.api.v1.reviews import router as review_router
from app.api.v1.like import router as like_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(review_router)
app.include_router(like_router)
app.include_router(search_router)
app.include_router(movie_router)
app.include_router(watchlist_router)
@app.get('/')
async def root():
    """Эндпоинт для проверки работы api"""
    return {'message': 'Home'}


