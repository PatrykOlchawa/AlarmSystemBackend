from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.common.enums import SensorType
from app.db.base import Base
from app.modules.readings.model import SensorReading

class Sensor(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )
    type: Mapped[SensorType] = mapped_column(
        Enum(SensorType),
        nullable=False
    )
    gpio_pin: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    enabled: Mapped[Boolean] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    location: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )
    readings: Mapped[list["SensorReading"]] = relationship(
        back_populates="sensor",
        cascade="all, delete-orphan"
    )
