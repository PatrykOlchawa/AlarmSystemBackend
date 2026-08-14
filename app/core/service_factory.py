from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.modules.sensors.repository import SensorRepository
from app.modules.sensors.service import SensorService

from app.modules.readings.repository import SensorReadingRepository
from app.modules.readings.service import SensorReadingService
from app.services.websocket_service import WebSocketMessageService
from app.modules.user_alarm.repository import UserAlarmRepository
from app.services.alarm_service import AlarmControlService
from app.modules.users.service import UserService
from app.security.hashing import PasswordHasher
from app.modules.users.repository import UserRepository
from app.modules.events.service import AlarmEventService
from app.modules.events.repository import AlarmEventRepository
from app.modules.notifications.service import NotificationService
from app.modules.notifications.repository import NotificationRepository
from app.modules.settings.service import SettingService
from app.modules.settings.repository import SettingRepository
from app.modules.auth.service import AuthService
from app.security.jwt_handler import JWTHandler 
from app.modules.devices.service import DeviceService
from app.modules.devices.repository import DeviceRepository
from app.services.device_control_service import DeviceControlService
from app.services.tollgate_service import TollgateService
from app.services.ocr_service import OCRService
from app.modules.car_plates.repository import CarPlateRepository
from app.modules.car_plates.service import CarPlateService
from app.modules.alarms.service import AlarmService
from app.modules.alarms.repository import AlarmRepository
from app.mqtt.service import mqtt_service
from app.modules.clients.repository import ClientRepository
from app.modules.clients.service import ClientService

class ServicesFactory:
    def create_session(self) -> Session:
        return SessionLocal()

    def create_user_service(
        self,
        db: Session,
    ) -> UserService:
        repository = UserRepository(db)
        password_hasher = PasswordHasher()
        return UserService(
            repository=repository,
            password_hasher=password_hasher,
            websocket_service=self.create_websocket_service(db)
        )

    
    def create_alarm_event_service(
        self,
        db: Session,
    ) -> AlarmEventService:
        repository = AlarmEventRepository(db) 
        return AlarmEventService(
            repository=repository,
            websocket_service=self.create_websocket_service(db)
        )

    def create_notification_service(
        self,
        db: Session,
    ) -> NotificationService:
        repository = NotificationRepository(db)
        return NotificationService(
            repository=repository,
            websocket_service=self.create_websocket_service(db)
        )

    def create_setting_service(
        self,
        db: Session,
    ) -> SettingService:
        repository = SettingRepository(db)
        return SettingService(
            repository=repository,
            websocket_service=self.create_websocket_service(db)
        )

    def create_auth_service(
        self,
        db: Session,
    ) -> AuthService:
        repository = UserRepository(db)
        password_hasher = PasswordHasher()
        jwt_handler = JWTHandler()
        return AuthService(repository, password_hasher, jwt_handler)

    def create_device_service(
        self,
        db: Session,
    ) -> DeviceService:
        repository = DeviceRepository(db)
        return DeviceService(
            repository=repository,
            websocket_service=self.create_websocket_service(db)
        )

    def create_device_control_service(
        self,
        db: Session,
    ) -> DeviceControlService:
        device_service = self.create_device_service(db)
        return DeviceControlService(device_service, mqtt_service)

    def create_ocr_service(
        self,
    ) -> OCRService:
        return OCRService()

    def create_car_plate_service(
        self,
        db:Session,
    ) -> CarPlateService:
        repository = CarPlateRepository(db)
        return CarPlateService(
            repository=repository,
            websocket_service=self.create_websocket_service(db)
        )
    
    def create_tollgate_service(
        self,
        db: Session,
    ) -> TollgateService:
        return TollgateService(
            self.create_device_control_service(db),
            self.create_ocr_service(),
            self.create_car_plate_service(db),
            self.create_setting_service(db),
            self.create_device_service(db)
        )

    def create_client_service(
        self,
        db: Session,
    ) -> ClientService:
        repository = ClientRepository(db)
        return ClientService(
            repository
        )
    def create_alarm_service(
        self,
        db: Session,
    ) -> AlarmService:
        repository = AlarmRepository(db)
        return AlarmService(
            repository=repository,
            user_alarm_repository=self.create_user_alarm_repository(db),
            client_service=self.create_client_service(db),
            user_repository=self.create_user_service(db),
            websocket_service=self.create_websocket_service(db),
        )
    
    def create_sensor_service(
        self,
        db: Session,
    ) -> SensorService:
        repository = SensorRepository(db)
        return SensorService(
            repository=repository,
            websocket_service=self.create_websocket_service(db)
        )

    def create_sensor_reading_service(
        self,
        db: Session,
    ) -> SensorReadingService:
        repository = SensorReadingRepository(db)

        return SensorReadingService(
            repository,
            self.create_sensor_service(db)
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

    def create_alarm_control_service(
        self,
        db: Session
    ) -> AlarmControlService:
        return AlarmControlService(
            settings_service=self.create_setting_service(db),
            sensor_service=self.create_sensor_service(db),
            alarm_event_service=self.create_alarm_event_service(db),
            notification_service=self.create_notification_service(db),
            user_service=self.create_user_service(db),
            auth_service=self.create_auth_service(db),
            device_service=self.create_device_service(db),
            device_control_service=self.create_device_control_service(db),
            tollgate_service=self.create_tollgate_service(db),
            alarm_service=self.create_alarm_service(db),
            websocket_service=self.create_websocket_service(db),
            user_alarm_repository=self.create_user_alarm_repository(db),
            mqtt_service=mqtt_service,
        )

    def create_sensor_handler(
        self,
        db: Session,
    ):
        from app.mqtt.handlers.sensor_handler import SensorHandler
        return SensorHandler(
            sensor_service=self.create_sensor_service(db),
            reading_service=self.create_sensor_reading_service(db),
            alarm_control_service=self.create_alarm_control_service(db),
            websocket_service=self.create_websocket_service(db),
        )

    def create_device_state_handler(
        self,
        db: Session,
    ):
        from app.mqtt.handlers.device_state_handler import StateHandler
        return StateHandler(
            device_service=self.create_device_service(db),
            websocket_service=self.create_websocket_service(db),
            alarm_service=self.create_alarm_service(db),
        )
  
    def create_alarm_state_handler(
        self,
        db: Session,
    ):
        from app.mqtt.handlers.alarm_state_handler import AlarmStateHandler
        return AlarmStateHandler(
            websocket_service=self.create_websocket_service(db),
            alarm_service=self.create_alarm_service(db),
        )