from app.modules.events.model import AlarmEvent
from app.modules.events.schemas import AlarmEventCreate
from app.modules.events.repository import AlarmEventRepository
from app.core.exceptions import AlarmEventNotFoundException
from app.common.enums import AlarmEventType

class AlarmEventService:
    def __init__(
        self,
        repository: AlarmEventRepository,
    ):
        self.repository = repository
    def get_all(self):
        return self.repository.get_all()
    def get_by_id(
        self,
        event_id: int
    ):
        event = self.repository.get_by_id(event_id)
        if event is None:
            raise AlarmEventNotFoundException()
        return event
    def get_latest(self):
        return self.repository.get_latest()

    def get_by_type(
        self,
        event_type: AlarmEventType,
    ):
        return self.repository.get_by_type(event_type)

    def create(
        self,
        request: AlarmEventCreate,
    ):
        event = AlarmEvent(
            event_type=request.event_type,
            user_id=request.user_id,
            device_id=request.device_id,
            location=request.location,
            message=request.message,
        )
        return self.repository.create(event)
        
    def delete(
        self,
        event_id: int,
    ):
        event = self.get_by_id(event_id)
        self.repository.delete(event)