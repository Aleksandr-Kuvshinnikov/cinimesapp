from datetime import datetime

from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func, ForeignKey, CheckConstraint


class Review(Base):
    __tablename__ = 'reviews'
    id:Mapped[int]= mapped_column(primary_key=True)
    user_id:Mapped[int]= mapped_column(ForeignKey('users.id'))
    movie_id:Mapped[int]= mapped_column(nullable=False)
    text:Mapped[str|None]= mapped_column(String(300), default=None)
    rating:Mapped[int]= mapped_column(nullable=False)
    created_at:Mapped[datetime]= mapped_column(nullable=False, server_default=func.now())
    is_active:Mapped[bool]= mapped_column(nullable= False, default= True)
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 10"),
    )





