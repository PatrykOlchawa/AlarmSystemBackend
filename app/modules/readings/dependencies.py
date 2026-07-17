from app.services.dependencies import get_alarm_service
from app.services.alarm_service import AlarmService
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.modules.sensors.dependencies import (
    get_sensor_service,
)
from app.modules.sensors.service import SensorService

from app.modules.readings.repository import (
    SensorReadingRepository,
)
from app.modules.readings.service import (
    SensorReadingService,
)
def get_sensor_reading_repository(
    db: Session = Depends(get_db),
) -> SensorReadingRepository:

    return SensorReadingRepository(db)


def get_sensor_reading_service(
    repository: SensorReadingRepository = Depends(
        get_sensor_reading_repository
    ),
    alarm_service: AlarmService = Depends(
        get_alarm_service
    ),
) -> SensorReadingService:

    return SensorReadingService(
        repository,
        alarm_service,
    )