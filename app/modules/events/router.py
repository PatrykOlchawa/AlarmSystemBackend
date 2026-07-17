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
    prefix="/alarm-events",
    tags=["Alarm Events"],
)

@router.get(
    "",
    response_model= list[AlarmEventRead],
)
def get_all_events(
    service: AlarmEventService = Depends(
        get_alarm_event_service,
    ),
):
    return service.get_all()

@router.get(
    "/last",
    response_model=AlarmEventRead,
)
def get_last_event(
    service: AlarmEventService = Depends(
        get_alarm_event_service,
    ),
):
    return service.get_latest()

@router.get(
    "/{event_id}",
    response_model=AlarmEventRead,
)
def get_event(
    event_id: int,
    service: AlarmEventService = Depends(
        get_alarm_event_service,
    ),
):
    return service.get_by_id(event_id)



@router.get(
    "/type/{event_type}",
    response_model=list[AlarmEventRead],
)
def get_events_by_type(
    event_type: AlarmEventType,
    service: AlarmEventService = Depends(
        get_alarm_event_service,
    ),
):
    return service.get_by_type(event_type)

@router.post(
    "",
    response_model=AlarmEventRead,
    status_code=status.HTTP_201_CREATED,
)

def create_event(
    request: AlarmEventCreate,
    service: AlarmEventService = Depends(
        get_alarm_event_service,
    ),
):
    return service.create(request)


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_event(
    event_id: int,
    service: AlarmEventService = Depends(
        get_alarm_event_service,
    ),
):
    service.delete(event_id)