from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.modules.sensors.repository import SensorRepository
from app.modules.sensors.service import SensorService

from app.modules.readings.repository import SensorReadingRepository
from app.modules.readings.service import SensorReadingService

from app.mqtt.handlers.sensor_handler import SensorHandler
from app.services.websocket_service import WebSocketMessageService
from app.modules.user_alarm.repository import UserAlarmRepository
class MQTTContainer:

    def create_session(self) -> Session:
        return SessionLocal()

    def create_sensor_service(
        self,
        db: Session,
    ) -> SensorService:
        repository = SensorRepository(db)
        return SensorService(repository)

    def create_sensor_reading_service(
        self,
        db: Session,
        sensor_service: SensorService,
    ) -> SensorReadingService:
        repository = SensorReadingRepository(db)

        return SensorReadingService(
            repository=repository,
            sensor_service=sensor_service,
        )
    def create_user_alarm_repository(
        self,
        db: Session,
    ) -> UserAlarmRepository:
        return UserAlarmRepository(db)

    def create_websocket_service(
        self,
        db: Session,
    ) -> WebSocketMessageService:
        return WebSocketMessageService(
            user_alarm_repository=self.create_user_alarm_repository(db),
        )
    
    def create_sensor_handler(
        self,
        db: Session,
    ) -> SensorHandler:
        sensor_service = self.create_sensor_service(db)

        reading_service = self.create_sensor_reading_service(
            db=db,
            sensor_service=sensor_service,
        )

        websocker_service = self.create_websocket_service(db)
        return SensorHandler(
            sensor_service=sensor_service,
            reading_service=reading_service,
            websocket_service=websocker_service,
        )


mqtt_container = MQTTContainer()