from app.security.authorization_dependencies import require_alarm_admin
from app.modules.alarms.model import Alarm
from app.security.auth_dependencies import get_current_user
from app.modules.users.model import User
import math as m
from app.modules.readings import service
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from app.modules.readings.dependencies import (
    get_sensor_reading_service,
)

from app.modules.readings.schemas import (
    SensorReadingCreate,
    SensorReadingRead,
)

from app.modules.readings.service import (
    SensorReadingService,
)

router = APIRouter(
    prefix="/alarms/{alarm_id}/sensors/{sensor_id}/readings",
    tags=["Sensor Readings"]
)


@router.get(
    "",
    response_model=list[SensorReadingRead]
)
def get_sensor_history(
    sensor_id: int,
    service: SensorReadingService = Depends(get_sensor_reading_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_all(alarm, sensor_id)

@router.get(
    "/last",
    response_model=SensorReadingRead | None
)
def get_last_reading(
    sensor_id: int,
    service: SensorReadingService = Depends(get_sensor_reading_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_latest(alarm, sensor_id)

@router.post(
    "",
    response_model=SensorReadingRead,
    status_code=status.HTTP_201_CREATED,
)
def create_reading(
    sensor_id: int,
    request: SensorReadingCreate,
    service: SensorReadingService = Depends(get_sensor_reading_service),
    alarm : Alarm = Depends(require_alarm_admin),

):
    return service.create(alarm, sensor_id, request)

@router.delete(
    "/{reading_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_reading(
    sensor_id: int,
    reading_id: int,
    service: SensorReadingService = Depends(get_sensor_reading_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    service.delete(alarm, sensor_id, reading_id)