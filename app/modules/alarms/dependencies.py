from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.alarms.repository import AlarmRepository
from app.modules.alarms.service import AlarmService
from app.modules.user_alarm.repository import UserAlarmRepository


def get_alarm_repository(
    db: Session = Depends(get_db),
) -> AlarmRepository:
    return AlarmRepository(db)

def get_user_alarm_repository(
    db: Session = Depends(get_db),
) -> UserAlarmRepository:
    return UserAlarmRepository(db)

def get_alarm_service(
    repository: AlarmRepository = Depends(get_alarm_repository),
    user_alarm_repository: UserAlarmRepository = Depends(get_user_alarm_repository),
) -> AlarmService:
    return AlarmService(repository, user_alarm_repository)