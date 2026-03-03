from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[str] = mapped_column(primary_key=True)
    creator_id: Mapped[str] = mapped_column()
    video_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    views_count: Mapped[int] = mapped_column()
    likes_count: Mapped[int] = mapped_column()
    comments_count: Mapped[int] = mapped_column()
    reports_count: Mapped[int] = mapped_column()

    video_snapshots: Mapped[list["VideoSnapshot"]] = relationship(
        back_populates="video"
    )
