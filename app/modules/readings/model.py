from app.db.base import Base
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.modules.sensors.model import Sensor

class SensorReading(Base):
    __tablename__ = "sensor_readings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    sensor_id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id"),
        nullable=False,
        index=True
    )
    value: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    sensor: Mapped["Sensor"] = relationship(
        back_populates="readings"
    )