from app.security.authorization_dependencies import require_alarm_admin
from app.modules.alarms.model import Alarm
from app.modules.alarm.schemas import AlarmPinRequest
from app.modules.alarm.schemas import AlarmMessageResponse
from fastapi import APIRouter, Depends, status
from app.modules.alarm.schemas import AlarmStatusResponse
from app.services.dependencies import get_alarm_service
from app.services.alarm_service import AlarmService
from app.modules.users.model import User
from app.security.auth_dependencies import get_current_user


router = APIRouter(
    prefix="/alarms/{alarm_id}",
    tags=["Alarm"],
)

@router.get(
    "/status",
    response_model=AlarmStatusResponse,
)
def get_alarm_status(
    service: AlarmService = Depends(get_alarm_service),
    alarm : Alarm = Depends(require_alarm_admin),   
):
    return AlarmStatusResponse(
        status=service.get_alarm_status(alarm)
    )

@router.post(
    "/arm",
    status_code=status.HTTP_200_OK,
)
def arm_alarm(
    request: AlarmPinRequest,
    current_user: User = Depends(get_current_user),
    alarm : Alarm = Depends(require_alarm_admin),
    service: AlarmService = Depends(get_alarm_service),
):
    service.arm_alarm(
        alarm,
        current_user.id,
        request.pin,
    )
    return AlarmMessageResponse(
        message="Alarm armed successfully",
    )

@router.post(
    "/disarm",
    status_code=status.HTTP_200_OK,
)
def disarm_alarm(
    request: AlarmPinRequest,
    current_user: User = Depends(get_current_user),
    service: AlarmService = Depends(get_alarm_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    service.disarm_alarm(
        alarm,
        current_user.id,
        request.pin,
    )
    return AlarmMessageResponse(
        message="Alarm disarmed successfully",
    )