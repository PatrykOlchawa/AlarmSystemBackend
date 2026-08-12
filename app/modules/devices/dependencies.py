from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.devices.repository import DeviceRepository
from app.modules.devices.service import DeviceService
from app.core.websocket.dependencies import get_websocket_service
from app.services.websocket_service import WebSocketMessageService

def get_device_repository(
    db: Session = Depends(get_db),
) -> DeviceRepository:
    return DeviceRepository(db)


def get_device_service(
    repository: DeviceRepository = Depends(get_device_repository),
    websocket_service: WebSocketMessageService= Depends(get_websocket_service),    
) -> DeviceService:
    return DeviceService(repository, websocket_service)