from app.db.base import Base
from sqlalchemy import (
    ForeignKey,
    String,
    Boolean,
    DateTime,
    Enum,
)
from sqlalchemy.orm import (
    relationship,
    mapped_column,
    Mapped,
)
from app.modules.alarms.model import Alarm
from datetime import datetime, timezone
from app.common.enums import ClientType
class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)

    alarm_id: Mapped[int] = mapped_column(
        ForeignKey("alarms.id", ondelete="CASCADE"),
        nullable=False,
    )

    client_id: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
        index=True,
    )

    secret_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    client_type: Mapped[ClientType] = mapped_column(
        Enum(ClientType),
        nullable=False
    )

    enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    creation_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=True,
    )

    alarm: Mapped["Alarm"] = relationship(
        back_populates="clients",
    )