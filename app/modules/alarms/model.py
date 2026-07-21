from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum
from datetime import datetime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.common.enums import AlarmStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.user_alarm.model import UserAlarm

class Alarm(Base):
    __tablename__ = "alarms"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(128),
        unique=False,
        nullable=False,
    )

    status: Mapped[AlarmStatus] = mapped_column(
        Enum(AlarmStatus),
        default=AlarmStatus.DISARMED,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    
    user_alarms: Mapped[list["UserAlarm"]] = relationship(
        back_populates="alarm",
        cascade="all, delete-orphan"
    )
