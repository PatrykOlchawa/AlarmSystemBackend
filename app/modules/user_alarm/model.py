from app.db.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from app.common.enums import AlarmRole
from sqlalchemy import Enum, ForeignKey, DateTime
from datetime import datetime


if TYPE_CHECKING:
    from app.modules.alarms.model import Alarm
    from app.modules.users.model import User
    
class UserAlarm(Base):
    __tablename__ = "user_alarm"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    alarm_id: Mapped[int] = mapped_column(
        ForeignKey("alarms.id"),
        primary_key=True,
    )

    role: Mapped[AlarmRole] = mapped_column(
        Enum(AlarmRole),
        nullable=False
    )

    joined_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="user_alarms",
    )

    alarm: Mapped["Alarm"] = relationship(
        back_populates="user_alarms",
    )