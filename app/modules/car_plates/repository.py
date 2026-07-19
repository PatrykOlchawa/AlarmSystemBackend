from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import CarPlate

class CarPlateRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[CarPlate]:
        stmt = select(CarPlate)
        return list(self.session.scalars(stmt).all())

    def get_by_id(
        self,
        car_plate_id: int
    ) -> CarPlate | None:
        stmt = (
            select(CarPlate)
            .where(CarPlate.id == car_plate_id)
        )
        return self.session.scalar(stmt)

    def get_by_plate_number(
        self,
        plate_number: str
    ) -> CarPlate | None:
        stmt = (
            select(CarPlate)
            .where(CarPlate.plate_number == plate_number)
        )
        return self.session.scalar(stmt)

    def get_by_owner(
        self,
        owner_name: str,
    ) -> list[CarPlate] | None:
        stmt = (
            select(CarPlate)
            .where(CarPlate.owner_name == owner_name)
        )
        return list(self.session.scalars(stmt).all())
    
    def get_authorized_plates(
        self,
    ) -> list[CarPlate] | None:
        stmt = (
            select(CarPlate)
            .where(CarPlate.auto_open == True)
        )
        return list(self.session.scalars(stmt).all())
    def create(
        self,
        car_plate: CarPlate
    ) -> CarPlate:
        self.session.add(car_plate)
        self.session.commit()
        self.session.refresh(car_plate)
        return car_plate

    def delete(
        self,
        car_plate: CarPlate
    ) -> None:
        self.session.delete(car_plate)
        self.session.commit()
        return None

    def update(
        self,
        car_plate: CarPlate
    ) -> CarPlate:
        self.session.commit()
        self.session.refresh(car_plate)
        return car_plate

    def is_authorized(
        self,
        plate_number: str,
    ) -> bool:
        car_plate = self.get_by_plate_number(plate_number)
        if car_plate is None:
            return False
        return car_plate.auto_open

