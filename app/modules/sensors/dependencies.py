from fastapi import Depends

from app.db.session import get_db

from sqlalchemy.orm import Session

from app.modules.sensors.repository import SensorRepository
from app.modules.sensors.service import SensorService


def get_sensor_repository(
    db: Session = Depends(get_db),
) -> SensorRepository:

    return SensorRepository(db)


def get_sensor_service(
    repository: SensorRepository = Depends(get_sensor_repository),
) -> SensorService:

    return SensorService(repository)