from sqlalchemy import ForeignKey
from app.modules.alarms.model import Alarm
from sqlalchemy.orm import relationship
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.common.enums import DeviceType
from app.common.enums import ConnectionType
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.events.model import AlarmEvent

class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)

    alarm_id: Mapped[int] = mapped_column(
        ForeignKey("alarms.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
        index=True
    )

    alarm_id: Mapped[int] = mapped_column(
        ForeignKey("alarms.id"),
        nullable=False
    )

    connection_type: Mapped[ConnectionType] = mapped_column(
        Enum(ConnectionType),
        nullable=False
    )
    connection_identifier: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    type: Mapped[DeviceType] = mapped_column(
        Enum(DeviceType),
        nullable=False
    )
    location: Mapped[str] = mapped_column(
        String(256),
        nullable=True
    )
    
    enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    alarm_events: Mapped[list["AlarmEvent"]] = relationship(
        back_populates="device"
    )

    alarm: Mapped["Alarm"] = relationship(
        back_populates="devices"
    )
    