from app.common.enums import AlarmRole
from app.common.enums import UserRole
from app.modules.users.model import User
from app.modules.alarms.repository import AlarmRepository
from app.modules.alarms.schemas import AlarmCreate
from app.modules.alarms.schemas import AlarmUpdate
from app.modules.alarms.model import Alarm
from app.core.exceptions import AlarmAlreadyExistsException
from app.core.exceptions import AlarmNotFoundException
from app.modules.user_alarm.repository import UserAlarmRepository
from app.modules.user_alarm.model import UserAlarm
class AlarmService:
    def __init__(
        self,
        repository: AlarmRepository,
        user_alarm_repository: UserAlarmRepository,
    ):
        self.repository = repository
        self.user_alarm_repository = user_alarm_repository

    def get_all(self) -> list[Alarm]:
        return self.repository.get_all()
    
    def get_by_id(
        self,
        alarm_id: int,
    ) -> Alarm | None:
        return self.repository.get_by_id(alarm_id)
    
    def get_all_by_user_id(
        self,
        user_id: int,
    ) -> list[Alarm]:
        return self.repository.get_all_by_user_id(user_id)
    
    def get_by_name(
        self,
        name: str,
    ) -> Alarm | None:
        return self.repository.get_by_name(name)
    
    def get_by_id_with_users(
        self,
        alarm_id: int,
    ) -> Alarm | None:
        alarm = self.repository.get_by_id_with_users(alarm_id)
        if alarm is None:
            raise AlarmNotFoundException()
        return alarm
    
    def create(
        self,
        request: AlarmCreate,
        current_user: User,
    ) -> Alarm:
        exist = self.get_by_name(request.name)
        if exist:
            raise AlarmAlreadyExistsException()
        alarm = Alarm(**request.model_dump())
        alarm =self.repository.create(alarm)
        membership = UserAlarm(
            alarm_id=alarm.id,
            user_id=current_user.id,
            role=AlarmRole.OWNER,
        )
        self.user_alarm_repository.create(membership)
        return alarm
    
    def update(
        self,
        alarm_id: int,
        request: AlarmUpdate,
    ) -> Alarm:
        alarm = self.get_by_id(alarm_id)
        if (
            request.name is not None
            and request.name != alarm.name
        ):
            exist = self.get_by_name(request.name)
            if exist:
                raise AlarmAlreadyExistsException()

        update_data = request.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(alarm, field, value)
        return self.repository.update(alarm)
    
    def delete(
        self,
        alarm_id: int,
    ) -> None:
        alarm = self.get_by_id(alarm_id)
        self.repository.delete(alarm)