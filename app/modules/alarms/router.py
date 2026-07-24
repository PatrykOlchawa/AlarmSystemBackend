from app.security.auth_dependencies import get_current_user
from app.modules.users.model import User
from fastapi import status
from app.common.schemas import MessageResponse
from fastapi import Depends
from fastapi import APIRouter
from app.modules.alarms.schemas import(
    AlarmResponse,
    AlarmUpdate,
    AlarmCreate,
    AddUser,
) 
from app.modules.alarms.service import AlarmService
from app.modules.alarms.dependencies import get_alarm_service
from app.modules.user_alarm.model import UserAlarm
from app.modules.user_alarm.repository import UserAlarmRepository 

router = APIRouter(
    prefix="/alarms",
    tags=["Alarms"],
)

@router.get(
    "/",
    response_model=list[AlarmResponse],    
)
def get_alarms(
    service: AlarmService = Depends(get_alarm_service),
    current_user: User = Depends(get_current_user),
) -> list[AlarmResponse]:
    return service.get_all()
    
@router.get(
    "/my",
    response_model=list[AlarmResponse],
)
def get_my_alarms(
    current_user: User = Depends(get_current_user),
    service: AlarmService = Depends(get_alarm_service),
) -> list[AlarmResponse]:
    return service.get_all_by_user_id(current_user.id)

@router.post(
    "/{alarm_id}/user",
    response_model=AlarmResponse,
)
def add_user_to_alarm(
    alarm_id: int,
    request: AddUser,
    service: AlarmService = Depends(get_alarm_service),
    current_user: User = Depends(get_current_user),
) -> MessageResponse:
    service.add_user_to_alarm(alarm_id, request)
    return MessageResponse(message="User added to alarm")
        
@router.get(
    "/{alarm_id}",
    response_model=AlarmResponse,
)
def get_alarm(
    alarm_id: int,
    service: AlarmService = Depends(get_alarm_service),
    current_user: User = Depends(get_current_user),
) -> AlarmResponse:
    return service.get_by_id(alarm_id)

@router.post(
    "/",
    response_model=AlarmResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_alarm(
    request: AlarmCreate,
    service: AlarmService = Depends(get_alarm_service),
    current_user: User = Depends(get_current_user),
) -> AlarmResponse:
    return service.create(request)


@router.patch(
    "/{alarm_id}",
    response_model=AlarmResponse,
)
def update_alarm(
    alarm_id: int,
    request: AlarmUpdate,
    service: AlarmService = Depends(get_alarm_service),
    current_user: User = Depends(get_current_user),
) -> AlarmResponse:
    return service.update(alarm_id, request)

@router.delete(
    "/{alarm_id}",
    response_model=MessageResponse,
)
def delete_alarm(
    alarm_id: int,
    service: AlarmService = Depends(get_alarm_service),
    current_user: User = Depends(get_current_user),
) -> MessageResponse:
    service.delete(alarm_id)
    return MessageResponse(message="Alarm deleted successfully")


