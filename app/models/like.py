from datetime import datetime

from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func, ForeignKey

class Like(Base):
    __tablename__ = 'likes'
    id:Mapped[int]= mapped_column(primary_key=True)
    user_id:Mapped[int]= mapped_column(ForeignKey('users.id'))
    movie_id:Mapped[int]= mapped_column(nullable=False)
    created_at:Mapped[datetime]= mapped_column(nullable=False, server_default=func.now())
    is_active:Mapped[bool]= mapped_column(default=True)