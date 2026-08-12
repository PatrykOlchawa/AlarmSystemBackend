from app.common.enums import (
    MessageEventType,
)
from app.core.exceptions import (
    CarPlateNotFoundException,
    WebsocketException,
)
from app.modules.alarms.model import Alarm
from app.modules.car_plates.schemas import CarPlateUpdate
from app.modules.car_plates.repository import CarPlateRepository
from app.modules.car_plates.model import CarPlate
from app.modules.car_plates.schemas import CarPlateCreate
from app.services.websocket_service import WebSocketMessageService


class CarPlateService:
    def __init__(
        self,
        repository: CarPlateRepository,
        websocket_service: WebSocketMessageService,        
    ):
        self.repository = repository
        self.websocket_service = websocket_service
    
    def get_all(
        self,
        alarm:Alarm
    ) -> list[CarPlate]:
        return self.repository.get_all(alarm.id)

    def get_by_id(
        self,
        alarm:Alarm,
        car_plate_id: int
    ) -> CarPlate:
        car_plate = self.repository.get_by_id(alarm.id, car_plate_id)
        if car_plate is None:
            raise CarPlateNotFoundException
        return car_plate
    
    def get_by_plate_number(
        self,
        alarm:Alarm,
        plate_number: str
    ) -> CarPlate:
        car_plate = self.repository.get_by_plate_number(alarm.id, plate_number)
        #if car_plate is None:
        #    raise CarPlateNotFoundException
        return car_plate

    def get_by_owner(
        self,
        alarm:Alarm,
        owner_name: str,
    ) -> list[CarPlate]:
        car_plate = self.repository.get_by_owner(alarm.id, owner_name)
        if car_plate is None:
            raise CarPlateNotFoundException
        return car_plate
    
    def get_authorized(
        self,
        alarm:Alarm
    ) -> list[CarPlate] | None:
        car_plates = self.repository.get_authorized_plates(alarm.id)
        if car_plates is None:
            raise CarPlateNotFoundException
        return car_plates
    
    def is_authorized(
        self,
        alarm:Alarm,
        plate_number: str,
    ) -> bool:
        return self.repository.is_authorized(alarm.id,plate_number)


    def create(
        self,
        alarm:Alarm,
        request: CarPlateCreate,
    ):
        car_plate = CarPlate(
            alarm_id = alarm.id,
            plate_number = request.plate_number,
            owner_name = request.owner_name,
            auto_open = request.auto_open
        )
        car_plate = self.repository.create(car_plate)
        self._notify_car_plates_changed(alarm_id=alarm.id)
        return car_plate
    
    def update(
        self,
        alarm:Alarm,
        car_plate_id: int,
        request: CarPlateUpdate,
    ) -> CarPlate:
        car_plate = self.get_by_id(alarm, car_plate_id)
        update_data = request.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(car_plate, field, value)
        car_plate = self.repository.update(alarm.id, car_plate)
        self._notify_car_plates_changed(alarm_id=alarm.id)
        return car_plate
    
    def delete(
        self,
        alarm:Alarm,
        car_plate_id: int,
    ):
        car_plate = self.get_by_id(alarm, car_plate_id)
        if car_plate is None:
            raise CarPlateNotFoundException
        self.repository.delete(alarm.id, car_plate)
        self._notify_car_plates_changed(alarm_id=alarm.id)

    def _notify_car_plates_changed(
        self,
        alarm_id: int,
    ) -> None:
        try:
            self.websocket_service.send_message_sync(
                alarm_id=alarm_id,
                event_type=MessageEventType.CAR_PLATES_CHANGED,
                data={},
            )
        except Exception:
            raise WebsocketException