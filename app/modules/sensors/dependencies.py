from fastapi import Depends

from app.db.session import get_db

from sqlalchemy.orm import Session

from app.modules.sensors.repository import SensorRepository
from app.modules.sensors.service import SensorService
from app.services.websocket_service import WebSocketMessageService
from app.core.websocket.dependencies import get_websocket_service
from app.mqtt.service import MQTTService
from app.mqtt.dependencies import get_mqtt_service

def get_sensor_repository(
    db: Session = Depends(get_db),
) -> SensorRepository:

    return SensorRepository(db)


def get_sensor_service(
    repository: SensorRepository = Depends(get_sensor_repository),
    websocket_service: WebSocketMessageService= Depends(get_websocket_service),
    mqtt_service: MQTTService = Depends(get_mqtt_service)
) -> SensorService:

    return SensorService(repository, websocket_service, mqtt_service)