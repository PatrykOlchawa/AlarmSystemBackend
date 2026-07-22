from app.modules.events.model import AlarmEvent
from app.modules.events.schemas import AlarmEventCreate
from app.modules.events.repository import AlarmEventRepository
from app.core.exceptions import AlarmEventNotFoundException
from app.common.enums import AlarmEventType
from app.modules.alarms.model import Alarm
class AlarmEventService:
    def __init__(
        self,
        repository: AlarmEventRepository,
    ):
        self.repository = repository
    def get_all(
        self,
        alarm:Alarm
    ):
        return self.repository.get_all(alarm)
    def get_by_id(
        self,
        alarm:Alarm,
        event_id: int
    ):
        event = self.repository.get_by_id(alarm,event_id)
        if event is None:
            raise AlarmEventNotFoundException()
        return event
    def get_latest(
        self, 
        alarm:Alarm
    ):
        return self.repository.get_latest(alarm)

    def get_by_type(
        self,
        alarm:Alarm,
        event_type: AlarmEventType,
    ):
        return self.repository.get_by_type(alarm,event_type)

    def create(
        self,
        alarm:Alarm,
        request: AlarmEventCreate,
    ):
        event = AlarmEvent(**request.model_dump(exclude={"alarm_id"}), alarm_id = alarm.id)
        return self.repository.create(event)
        
    def delete(
        self,
        alarm:Alarm,
        event_id: int,
    ):
        event = self.get_by_id(alarm,event_id)
        self.repository.delete(event)