from datetime import datetime

from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func, ForeignKey, Boolean


class WatchList(Base):
    __tablename__ = 'watchlist'
    id:Mapped[int]= mapped_column(primary_key=True)
    movie_id:Mapped[int]= mapped_column(nullable=False)
    status:Mapped[str]= mapped_column(String(50), nullable=False)
    created_at:Mapped[datetime]= mapped_column(DateTime, server_default=func.now())
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    is_active:Mapped[bool]= mapped_column(Boolean, nullable=True, default=True)
