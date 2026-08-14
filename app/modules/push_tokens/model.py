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
from datetime import datetime
from app.common.enums import UserRole
from app.modules.events.model import AlarmEvent
from app.modules.notifications.model import Notification
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

    platform: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    is_active: Mapped[Boolean] = mapped_column(
        Boolean,
        default=True
    )

    user: Mapped["User"] = relationship(
        back_populates="push_tokens",
    )