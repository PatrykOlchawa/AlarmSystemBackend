from app.db.base import Base
from sqlalchemy import(
    Boolean,
    DateTime,
    Enum,
    String,
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
    from app.modules.user_alarm.model import UserAlarm
    from app.modules.push_tokens.model import PushToken

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    creation_date: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.utcnow(),
        nullable=True
    )

    alarm_events: Mapped[list["AlarmEvent"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    user_alarms: Mapped[list["UserAlarm"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    push_tokens: Mapped[list["PushToken"]] = relationship(
        "PushToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )