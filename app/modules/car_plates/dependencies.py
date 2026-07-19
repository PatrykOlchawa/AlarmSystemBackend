from fastapi import Depends

from app.db.session import get_db

from sqlalchemy.orm import Session

from app.modules.car_plates.repository import CarPlateRepository
from app.modules.car_plates.service import CarPlateService

def get_car_plate_repository(
    db: Session = Depends(get_db),
) -> CarPlateRepository:
    return CarPlateRepository(db)

def get_car_plate_service(
    repository: CarPlateRepository = Depends(get_car_plate_repository),
) -> CarPlateService:
    return CarPlateService(repository)
