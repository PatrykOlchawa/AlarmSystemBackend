from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.user_alarm.repository import UserAlarmRepository

def get_user_alarm_repository(
    db: Session = Depends(get_db),
) -> UserAlarmRepository:
    return UserAlarmRepository(db)
