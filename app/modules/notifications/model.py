from sqlalchemy.orm import relationship
from sqlalchemy import Enum
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from app.common.enums import NotificationType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.users.model import User
    from app.modules.alarms.model import Alarm

class Notification(Base):

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    alarm_id: Mapped[int] = mapped_column(
        ForeignKey("alarms.id"),
        nullable=False,
        index=True
    )
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    notification_type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType),
        nullable=False
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    user: Mapped["User | None"] = relationship(
        back_populates="notifications"
    )

    alarm: Mapped["Alarm"] = relationship(
        back_populates="notifications",
    )