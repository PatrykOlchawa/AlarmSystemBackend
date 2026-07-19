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

router = APIRouter(
    prefix="/car-plates",
    tags=["Car Plates"],
)

@router.get(
    "",
    response_model=list[CarPlateRead]
)
def get_all_car_plates(
    service: CarPlateService = Depends(get_car_plate_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_all()



@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CarPlateRead,
)
def create_car_plate(
    request: CarPlateCreate,
    service: CarPlateService = Depends(get_car_plate_service),
    current_user: User = Depends(get_current_user),
):
    return service.create_car_plate(request)
    
@router.get(
    "/is-authorized/{plate_number}",
    response_model=bool
)
def is_authorized(
    plate_number: str,
    service: CarPlateService = Depends(get_car_plate_service),
    current_user: User = Depends(get_current_user),
):
    return service.is_authorized(plate_number)


@router.get(
    "/authorized",
    response_model=list[CarPlateRead],

)
def get_authorized_plates(
    service: CarPlateService = Depends(get_car_plate_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_authorized_plates()
    
@router.get(
    "/{car_plate_id}",
    response_model=CarPlateRead
)
def get_car_plate(
    car_plate_id: int,
    service: CarPlateService = Depends(get_car_plate_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_by_id(car_plate_id)

@router.patch(
    "/{car_plate_id}",
    response_model=CarPlateRead,
)
def update_car_plate(
    car_plate_id: int,
    request: CarPlateUpdate,
    service: CarPlateService = Depends(get_car_plate_service),
    current_user: User = Depends(get_current_user),
):
    return service.update_car_plate(car_plate_id, request)

@router.delete(
    "/{car_plate_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_car_plate(
    car_plate_id: int,
    service: CarPlateService = Depends(get_car_plate_service),
    current_user: User = Depends(get_current_user),
):
    return service.delete_car_plate(car_plate_id)

