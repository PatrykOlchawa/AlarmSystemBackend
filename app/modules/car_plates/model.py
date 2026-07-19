from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


from app.db.base import Base

class CarPlate(Base):
    __tablename__ = "car_plates"

    id: Mapped[int] = mapped_column(primary_key=True)
    
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
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )