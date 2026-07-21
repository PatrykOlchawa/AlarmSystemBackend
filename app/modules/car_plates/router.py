from app.security.auth_dependencies import get_current_user
from app.modules.users.model import User
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from app.modules.car_plates.dependencies import get_car_plate_service
from app.modules.car_plates.schemas import (
    CarPlateCreate,
    CarPlateUpdate,
    CarPlateRead,
)
from app.modules.car_plates.service import CarPlateService
from app.security.authorization_dependencies import require_alarm_admin
from app.modules.alarms.model import Alarm

router = APIRouter(
    prefix="/alarms/{alarm_id}/car-plates",
    tags=["Car Plates"],
)

@router.get(
    "",
    response_model=list[CarPlateRead]
)
def get_all(    
    service: CarPlateService = Depends(get_car_plate_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_all(alarm)



@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CarPlateRead,
)
def create(
    request: CarPlateCreate,
    service: CarPlateService = Depends(get_car_plate_service),
    alarm : Alarm = Depends(require_alarm_admin),

):
    return service.create(alarm,request)
    


@router.get(
    "/authorized",
    response_model=list[CarPlateRead],

)
def get_authorized(
    service: CarPlateService = Depends(get_car_plate_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_authorized(alarm)

@router.get(
    "/check/{plate_number}",
    response_model=bool
)
def is_authorized(
    plate_number: str,
    service: CarPlateService = Depends(get_car_plate_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.is_authorized(alarm, plate_number)
   
@router.get(
    "/{car_plate_id}",
    response_model=CarPlateRead
)
def get_by_id(
    car_plate_id: int,
    service: CarPlateService = Depends(get_car_plate_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_by_id(alarm,car_plate_id)

@router.patch(
    "/{car_plate_id}",
    response_model=CarPlateRead,
)
def update(
    car_plate_id: int,
    request: CarPlateUpdate,
    service: CarPlateService = Depends(get_car_plate_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.update(alarm,car_plate_id, request)

@router.delete(
    "/{car_plate_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    car_plate_id: int,
    service: CarPlateService = Depends(get_car_plate_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.delete(alarm,car_plate_id)

