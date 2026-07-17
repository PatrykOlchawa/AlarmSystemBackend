from sqlalchemy.orm import relationship
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.common.enums import AlarmEventType
from app.db.base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.modules.users.model import User
    from app.modules.devices.model import Device


class AlarmEvent(Base):
    __tablename__ = "alarm_events"

    id: Mapped[int] = mapped_column(primary_key=True)

    event_type: Mapped[AlarmEventType] = mapped_column(
        Enum(AlarmEventType),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )
    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id"),
        nullable=True,
        index=True
    )

    location: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    message: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    user: Mapped["User | None"] = relationship(
        back_populates="alarm_events"
    )

    device: Mapped["Device | None"] = relationship(
        back_populates="alarm_events"
    )