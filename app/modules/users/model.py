from sqlalchemy.orm import relationship
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from app.common.enums import UserRole
from app.modules.events.model import AlarmEvent
from app.modules.notifications.model import Notification

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

    pin_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole),
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