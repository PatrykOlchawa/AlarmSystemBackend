from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.alarms.repository import AlarmRepository
from app.modules.alarms.service import AlarmService
from app.modules.user_alarm.repository import UserAlarmRepository
from app.modules.clients.service import ClientService
from app.modules.clients.dependencies import get_client_service
from app.modules.users.dependencies import get_user_repository
from app.services.websocket_service import WebSocketMessageService
from app.core.websocket.dependencies import get_websocket_service


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
    client_service: ClientService = Depends(get_client_service),
    user_repository: ClientService = Depends(get_user_repository),
    websocket_service: WebSocketMessageService= Depends(get_websocket_service),    

) -> AlarmService:
    return AlarmService(
        repository=repository,
        user_alarm_repository=user_alarm_repository,
        client_service=client_service,
        user_repository = user_repository,
        websocket_service=websocket_service
    )