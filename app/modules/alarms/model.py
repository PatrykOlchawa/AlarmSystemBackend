
from app.modules.settings.model import Setting

from app.modules.notifications.model import Notification
from app.modules.car_plates.model import CarPlate
from app.modules.sensors.model import Sensor
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
    from app.modules.devices.model import Device
    from app.modules.events.model import AlarmEvent

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

    devices: Mapped[list["Device"]] = relationship(
        back_populates="alarm",
    )

    sensors: Mapped[list["Sensor"]] = relationship(
        back_populates="alarm",
    )

    car_plates: Mapped[list["CarPlate"]] = relationship(
        back_populates="alarm",
    )

    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="alarm",
    )

    events: Mapped[list["AlarmEvent"]] = relationship(
        back_populates="alarm",
    )

    settings: Mapped[list["Setting"]] = relationship(
        back_populates="alarm",
    )
    