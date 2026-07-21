from app.security.authorization_dependencies import require_alarm_admin
from app.modules.alarms.model import Alarm
from app.security.auth_dependencies import get_current_user
from app.modules.users.model import User
from fastapi import APIRouter, Depends, status

from app.common.enums import AlarmEventType

from app.modules.events.dependencies import (
    get_alarm_event_service,
)

from app.modules.events.schemas import (
    AlarmEventCreate,
    AlarmEventRead,
)

from app.modules.events.service import (
    AlarmEventService,
)

router = APIRouter(
    prefix="/alarms/{alarm_id}/alarm-events",
    tags=["Alarm Events"],
)

@router.get(
    "",
    response_model= list[AlarmEventRead],
)
def get_all_events(
    service: AlarmEventService = Depends(get_alarm_event_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_all(alarm)

@router.get(
    "/last",
    response_model=AlarmEventRead,
)
def get_last_event(
    service: AlarmEventService = Depends(get_alarm_event_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_latest(alarm)

@router.get(
    "/{event_id}",
    response_model=AlarmEventRead,
)
def get_event(
    event_id: int,
    service: AlarmEventService = Depends(get_alarm_event_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_by_id(alarm,event_id)



@router.get(
    "/type/{event_type}",
    response_model=list[AlarmEventRead],
)
def get_events_by_type(
    event_type: AlarmEventType,
    service: AlarmEventService = Depends(get_alarm_event_service),
    alarm : Alarm = Depends(require_alarm_admin)
):
    return service.get_by_type(alarm,event_type)

@router.post(
    "",
    response_model=AlarmEventRead,
    status_code=status.HTTP_201_CREATED,
)

def create_event(
    request: AlarmEventCreate,
    service: AlarmEventService = Depends(get_alarm_event_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.create(alarm,request)


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_event(
    event_id: int,
    service: AlarmEventService = Depends(get_alarm_event_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    service.delete(alarm,event_id)