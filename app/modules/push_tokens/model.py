from app.db.base import Base
from sqlalchemy import(
    Boolean,
    DateTime,
    Enum,
    String,
    ForeignKey,
    Text
) 
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,

)
from datetime import datetime, timezone
from app.common.enums import PushPlatform, PushLocale
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.modules.users.model import User

class PushToken(Base):
    __tablename__ = "push_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    token: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    platform: Mapped[PushPlatform] = mapped_column(
        Enum(PushPlatform),
        nullable=False
    )

    locale: Mapped[PushLocale] = mapped_column(
        Enum(PushLocale),
        nullable=False
    )

    device_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default= lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default= lambda: datetime.now(timezone.utc),
        onupdate= lambda: datetime.now(timezone.utc),
        nullable=False
    )

    is_active: Mapped[Boolean] = mapped_column(
        Boolean,
        default=True
    )

    user: Mapped["User"] = relationship(
        back_populates="push_tokens",
    )