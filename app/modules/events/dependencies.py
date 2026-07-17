from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.modules.events.repository import (
    AlarmEventRepository,
)

from app.modules.events.service import (
    AlarmEventService,
)


def get_alarm_event_repository(
    db: Session = Depends(get_db),
) -> AlarmEventRepository:
    return AlarmEventRepository(db)

def get_alarm_event_service(
    repository: AlarmEventRepository = Depends(get_alarm_event_repository),
) -> AlarmEventService:
    return AlarmEventService(repository)