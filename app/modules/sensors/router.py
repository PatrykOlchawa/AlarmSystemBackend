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
    prefix="/sensors",
    tags=["Sensors"],
)

@router.get(
    "",
    response_model=list[SensorRead]
)
def get_all_sensors(
    service: SensorService = Depends(get_sensor_service)
):
    return service.get_all_sensors()

@router.get(
    "/{sensor_id}",
    response_model=SensorRead
)
def get_sensor(
    sensor_id: int,
    service: SensorService = Depends(get_sensor_service)
):
    return service.get_sensor_by_id(sensor_id)

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=SensorRead,
)
def create_sensor(
    request: SensorCreate,
    service: SensorService = Depends(get_sensor_service)
):
    return service.create_sensor(request)

@router.patch(
    "/{sesor_id}",
    response_model=SensorRead,

)
def update_sensor(
    sensor_id: int,
    request: SensorUpdate,
    service: SensorService = Depends(get_sensor_service),
):
    return service.update_sensor(sensor_id, request)

@router.delete(
    "/{sensor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_sensor(
    sensor_id: int,
    service: SensorService = Depends(get_sensor_service),
):
    return service.delete_sensor(sensor_id)
    