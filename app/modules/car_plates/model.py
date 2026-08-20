import typing
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from datetime import datetime, timezone
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey

from app.db.base import Base

if typing.TYPE_CHECKING:
    from app.modules.alarms.model import Alarm


class CarPlate(Base):
    __tablename__ = "car_plates"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    alarm_id: Mapped[int] = mapped_column(
        ForeignKey("alarms.id", ondelete="CASCADE"),
        nullable=False
    )

    plate_number: Mapped[str] = mapped_column(
        String(7),
        unique=True,
        nullable=False,
        index=True
    )
    
    owner_name: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    
    auto_open: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    alarm: Mapped["Alarm"] = relationship(
        back_populates="car_plates",
    )