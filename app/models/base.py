from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    # created_at: Mapped[datetime] = mapped_column(default=func.now())
    # updated_at: Mapped[datetime] = mapped_column(
    #     default=func.now(),
    #     onupdate=func.now(),
    # )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
