from app.security.authorization_dependencies import require_alarm_admin
from app.modules.alarms.model import Alarm
from app.security.auth_dependencies import get_current_user
from app.modules.users.model import User
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from app.modules.sensors.dependencies import get_sensor_service
from app.modules.sensors.schemas import (
    SensorCreate,
    SensorUpdate,
    SensorRead,
)
from app.modules.sensors.service import SensorService

router = APIRouter(
    prefix="/alarms/{alarm_id}/sensors",
    tags=["Sensors"],
)

@router.get(
    "",
    response_model=list[SensorRead]
)
def get_all_sensors(
    service: SensorService = Depends(get_sensor_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_all_sensors(alarm)

@router.get(
    "/{sensor_id}",
    response_model=SensorRead
)
def get_sensor(
    sensor_id: int,
    service: SensorService = Depends(get_sensor_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_sensor_by_id(alarm, sensor_id)

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=SensorRead,
)
def create_sensor(
    request: SensorCreate,
    service: SensorService = Depends(get_sensor_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.create_sensor(alarm, request)

@router.patch(
    "/{sensor_id}",
    response_model=SensorRead,

)
def update_sensor(
    sensor_id: int,
    request: SensorUpdate,
    service: SensorService = Depends(get_sensor_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.update_sensor(alarm, sensor_id, request)

@router.delete(
    "/{sensor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_sensor(
    sensor_id: int,
    service: SensorService = Depends(get_sensor_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.delete_sensor(alarm, sensor_id)
    