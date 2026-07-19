from app.modules.car_plates.schemas import CarPlateUpdate
from app.core.exceptions import CarPlateNotFoundException
from app.modules.car_plates.repository import CarPlateRepository
from app.modules.car_plates.model import CarPlate
from app.modules.car_plates.schemas import CarPlateCreate

class CarPlateService:
    def __init__(
        self,
        repository: CarPlateRepository
    ):
        self.repository = repository

    def get_all(self) -> list[CarPlate]:
        return self.repository.get_all()

    def get_by_id(
        self,
        car_plate_id: int
    ) -> CarPlate:
        car_plate = self.repository.get_by_id(car_plate_id)
        if car_plate is None:
            raise CarPlateNotFoundException
        return car_plate
    
    def get_by_plate_number(
        self,
        plate_number: str
    ) -> CarPlate:
        car_plate = self.repository.get_by_plate_number(plate_number)
        #if car_plate is None:
        #    raise CarPlateNotFoundException
        return car_plate

    def get_by_owner(
        self,
        owner_name: str,
    ) -> list[CarPlate]:
        car_plate = self.repository.get_by_owner(owner_name)
        if car_plate is None:
            raise CarPlateNotFoundException
        return car_plate

    def create_car_plate(
        self,
        request: CarPlateCreate,
    ):
        car_plate = CarPlate(
            plate_number = request.plate_number,
            owner_name = request.owner_name,
            auto_open = request.auto_open
        )
        return self.repository.create(car_plate)

    def update_car_plate(
        self,
        car_plate_id: int,
        request: CarPlateUpdate,
    ) -> CarPlate:
        car_plate = self.get_by_id(car_plate_id)
        update_data = request.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(car_plate, field, value)
        return self.repository.update(car_plate)

    def delete_car_plate(
        self,
        car_plate_id: int,
    ):
        car_plate = self.get_by_id(car_plate_id)
        if car_plate is None:
            raise CarPlateNotFoundException
        self.repository.delete(car_plate)
    
    def is_authorized(
        self,
        plate_number: str,
    ) -> bool:
        return self.repository.is_authorized(plate_number)

    def get_authorized_plates(self) -> list[CarPlate] | None:
        car_plates = self.repository.get_authorized_plates()
        if car_plates is None:
            raise CarPlateNotFoundException
        return car_plates