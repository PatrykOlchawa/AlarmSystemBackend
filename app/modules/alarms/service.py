from app.core.exceptions import AlarmAccessDeniedException
from app.common.enums import (
    AlarmRole,
    AlarmStatus,
    UserRole
)
from app.modules.users.model import User
from app.modules.alarms.repository import AlarmRepository
from app.modules.alarms.schemas import (
    AlarmCreate,
    AlarmUpdate,
    AddUser,
    DeleteUser,
) 
from app.modules.alarms.model import Alarm
from app.core.exceptions import (
    AlarmAlreadyExistsException,
    AlarmNotFoundException,
    UserNotFoundException,
    UserAlreadyAddedToAlarm,
    UserNotAddedToAlarm,
)
from app.modules.user_alarm.repository import UserAlarmRepository
from app.modules.user_alarm.model import UserAlarm
from app.modules.users.service import UserService

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

    def get_user_alarm_role(
        self,
        alarm_id,
        user_id,
    ) -> AlarmRole:
        return self.repository.get_alarm_role(alarm_id, user_id)
    
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
    def set_alarm_status(
        self,
        alarm: Alarm,
        alarm_status: AlarmStatus,
    ):
        self.repository.set_alarm_status(alarm, alarm_status)

    def update_alarm_role(
        self,
        alarm_id: int,
        user_id: int,
        user_alarm_role: AlarmRole,
    ):
        self.repository.update_alarm_role(alarm_id, user_id, user_alarm_role)
    def create(
        self,
        request: AlarmCreate,
    ) -> Alarm:
        exist = self.get_by_name(request.name)
        if exist:
            raise AlarmAlreadyExistsException() 
        alarm = Alarm(**request.model_dump())
        self.repository.create(alarm)
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

    def add_user_to_alarm(
        self,
        alarm_id: int,
        user_id: int,
        alarm_role: AlarmRole,
    ) -> None:
        membership = self.user_alarm_repository.get(user_id, alarm_id)
        if membership:
            raise UserAlreadyAddedToAlarm()
        
        membership = UserAlarm(
            alarm_id=alarm_id,
            user_id=user_id,
            role=alarm_role,
        )
        self.user_alarm_repository.create(membership)

    def delete_user_from_alarm(
        self,
        alarm_id: int,
        user_id: int,
    ) -> None:
        membership = self.user_alarm_repository.get(user_id, alarm_id)
        if not membership:
            raise UserNotAddedToAlarm()
        self.user_alarm_repository.delete(membership)

    def verify_alarm_access(
        self,
        alarm_id: int,
        current_user: User,
        required_role: set[AlarmRole] | None = None,
    ) -> None:
        alarm = self.get_by_id(alarm_id)
        if alarm is None:
            raise AlarmNotFoundException()

        membership = self.user_alarm_repository.get(
            user_id=current_user.id,
            alarm_id=alarm_id,
        )

        if membership is None: 
            raise AlarmAccessDeniedException()
        if required_role is not None and membership.role not in required_role:
            raise AlarmAccessDeniedException()
        
        return alarm