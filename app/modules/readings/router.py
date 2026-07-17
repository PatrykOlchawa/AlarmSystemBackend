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
    prefix="/sensor-readings",
    tags=["Sensor Readings"]
)


@router.get(
    "",
    response_model = list[SensorReadingRead],
)
def get_all_readings(
    serivce: SensorReadingRead = Depends(
        get_sensor_reading_service
    ),
):
    return serivce.get_all()

@router.get(
    "/sensor/{sensor_id}",
    response_model=list[SensorReadingRead]
)
def get_sensor_hisory(
    sensor_id: int,
    service: SensorReadingService = Depends(
        get_sensor_reading_service
    ),
):
    return service.get_by_sensor(sensor_id)

@router.get(
    "/sensor/{sensor_id}/last",
    response_model=SensorReadingRead | None
)
def get_last_reading(
    sensor_id: int,
    service: SensorReadingService = Depends(
        get_sensor_reading_service
    ),
):
    return service.get_latest_by_sensor(sensor_id)

@router.post(
    "",
    response_model=SensorReadingRead,
    status_code=status.HTTP_201_CREATED,
)
def create_reading(
    request: SensorReadingCreate,
    service: SensorReadingService = Depends(
        get_sensor_reading_service
    ),
):
    return service.create(request)

@router.delete(
    "/{reading_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_reading(
    reading_id: int,
    service: SensorReadingService = Depends(
        get_sensor_reading_service
    ),
):
    service.delete(reading_id)