from app.modules.alarms.model import Alarm
from app.services.tollgate_service import TollgateService
from app.services import tollgate_service
from app.modules.devices.service import DeviceService
from app.services.device_control_service import DeviceControlService
from app.core.exceptions import InvalidPinException, AlarmAccessDeniedException
from app.modules.auth.service import AuthService
from app.core.exceptions import AlarmAlreadyDisarmedException
from app.core.exceptions import InvalidAlarmStateException
from app.modules.notifications.schemas import NotificationCreate
from app.common.enums import (
    NotificationType,
    MessageEventType,
    AlarmEventType,
    SensorType,
    AlarmStatus,
    DeviceType,
)
from app.modules.events.model import AlarmEvent
from app.modules.sensors.model import Sensor
from app.modules.readings.model import SensorReading
from app.modules.settings.service import SettingService
from app.modules.sensors.service import SensorService
from app.modules.events.service import AlarmEventService
from app.modules.notifications.service import NotificationService
from app.modules.readings.service import SensorReadingService
from app.modules.users.service import UserService
from app.security.hashing import password_hasher
from app.modules.devices.service import DeviceService
#from app.modules.devices.service import DeviceService
from app.modules.events.schemas import AlarmEventCreate
from app.modules.alarms.service import AlarmService
from app.modules.user_alarm.repository import UserAlarmRepository
from app.core.websocket.manager import connection_manager
from app.services.websocket_service import WebSocketMessageService
from app.services.push_tokens_service import PushNotificationService
from app.mqtt.service import MQTTService
from app.core.event_loop import get_event_loop
import asyncio
import logging
logger = logging.getLogger(__name__)
class AlarmControlService:
    def __init__(
        self,
        settings_service: SettingService,
        sensor_service: SensorService,
        alarm_event_service: AlarmEventService,
        notification_service: NotificationService,
        user_service: UserService,
        auth_service: AuthService,
        device_service: DeviceService,
        device_control_service: DeviceControlService,
        tollgate_service: TollgateService,
        alarm_service: AlarmService,
        websocket_service: WebSocketMessageService,
        user_alarm_repository: UserAlarmRepository,
        mqtt_service: MQTTService,
        push_notification_service: PushNotificationService,
    ):
        self.settings_service = settings_service
        self.sensor_service = sensor_service
        self.alarm_event_service = alarm_event_service
        self.notification_service = notification_service
        self.user_service = user_service
        self.auth_service = auth_service
        self.device_control_service = device_control_service
        self.device_service = device_service
        self.tollgate_service = tollgate_service
        self.alarm_service = alarm_service
        self.user_alarm_repository = user_alarm_repository
        self.websocket_service = websocket_service
        self.mqtt_service = mqtt_service
        self.push_notification_service = push_notification_service
    def process_sensor_reading(
        self,
        alarm_id: int,
        reading: SensorReading,
    ) -> None:
        logger.info(
            "process_sensor_reading alarm=%s sensor=%s value=%s",
            alarm_id,
            reading.sensor_id,
            reading.value,
        )
        alarm = self.alarm_service.get_by_id(alarm_id)
        sensor = self.sensor_service.get_sensor_by_id(alarm, reading.sensor_id)
        if sensor is None:
            return
        logger.info(
            "Alarm status=%s expected=%s",
            alarm.status,
            AlarmStatus.ARMED,
        )

        self.websocket_service.send_message_sync(
            alarm_id=alarm.id,
            event_type=MessageEventType.NEW_READING,
            data={
                "alarm_id": alarm.id,
                "reading_id": reading.id,
                "value": reading.value,
                "timestamp": reading.timestamp,
                "sensor_id":sensor.id,
                "gpio_pin": sensor.gpio_pin,
                "location": sensor.location,
            }
        )

        if alarm.status != AlarmStatus.ARMED:
            return
        
        match sensor.type:
            case SensorType.PIR:
                triggered = self._process_motion(reading)
            case SensorType.LDR:
                triggered = self._process_ldr(reading)
            case SensorType.DHT11:
                triggered = self._process_dht11(reading)
            case _:
                return
        logger.info(
            "Sensor type=%s value=%s",
            sensor.type,
            reading.value,
        )    
        logger.info(
            "triggered=%s",
            triggered,
        )
        if not triggered:
            return
        self._trigger_alarm(
            alarm=alarm,
            sensor=sensor,
        )
    def _process_motion(
        self,
        reading: SensorReading
    ):
        return reading.value == 1

    def _process_ldr(
        self,
        reading: SensorReading,
    ):
        return reading.value < reading.sensor.threshold
    
    def _process_dht11(
        self,
        reading: SensorReading,
    ):
        return reading.value < reading.sensor.threshold
    async def arm_alarm(
        self,
        alarm: Alarm,
        user_id:int,
        pin:str,
    ) -> None:
        membership = self.user_alarm_repository.get(
                    alarm_id=alarm.id,
                    user_id=user_id
                )
        if membership is None:
            raise AlarmAccessDeniedException
        
        if not password_hasher.verify_pin(pin, membership.pin_hash):
            raise InvalidPinException()
        
        alarm_status = alarm.status
        if alarm_status != AlarmStatus.DISARMED:
            raise InvalidAlarmStateException(alarm_status)

        self.alarm_service.set_alarm_status(alarm, AlarmStatus.ARMED)

        await self.websocket_service.send_message(
            alarm_id=alarm.id,
            event_type=MessageEventType.ALARM_STATUS_CHANGED,
            data={
                "status": alarm.status.value,
            }
        )
        event = self._create_event(
            event_type=AlarmEventType.ALARM_ARMED,
            message="Alarm armed",
            user_id=user_id,
            device_id=None,
            location=None,
            alarm=alarm,
        )
        self._notify_users(
            title="Alarm armed",
            message="The alarm system has been armed",
            event_id=event.id,
            alarm=alarm,
        )
        self.mqtt_service.publish_alarm_command(
            alarm_id=alarm.id,
            state=AlarmStatus.ARMED,
        )
        #self.tollgate_service.process_vehicle()
    
    async def disarm_alarm(
        self,
        alarm: Alarm,
        user_id:int,
        pin:str,
    ) -> None:
        membership = self.user_alarm_repository.get(
            alarm_id=alarm.id,
            user_id=user_id
        )
        if membership is None:
            raise AlarmAccessDeniedException
        
        if not password_hasher.verify_pin(pin, membership.pin_hash):
            raise InvalidPinException()
            
        if alarm.status == AlarmStatus.DISARMED:
            raise AlarmAlreadyDisarmedException()
        
        self.alarm_service.set_alarm_status(alarm, AlarmStatus.DISARMED)

        await self.websocket_service.send_message(
            alarm_id=alarm.id,
            event_type=MessageEventType.ALARM_STATUS_CHANGED,
            data={
                "status": alarm.status.value,
            }
        )
        event = self._create_event(
            event_type=AlarmEventType.ALARM_DISARMED,
            message="Alarm disarmed",
            user_id=user_id,
            device_id=None,
            location=None,
            alarm=alarm,
        )
        self._notify_users(
            title="Alarm disarmed",
            message="The alarm system has been disarmed",
            event_id=event.id,
            alarm=alarm,
        )
        self.mqtt_service.publish_alarm_command(
            alarm_id=alarm.id,
            state=AlarmStatus.DISARMED,
        )
    
    def _trigger_alarm(
        self,
        sensor: Sensor,
        alarm: Alarm,
    ) -> None:

        if alarm.status in (
            AlarmStatus.ACTIVATED,
        ):
            return
        
        self.alarm_service.set_alarm_status(alarm, AlarmStatus.TRIGGERED)

        self.mqtt_service.publish_alarm_command(
                alarm_id=alarm.id,
                state=AlarmStatus.TRIGGERED,
        )
        
        self.websocket_service.send_message_sync(
            alarm_id=alarm.id,
            event_type=MessageEventType.ALARM_STATUS_CHANGED,
            data={
                "status": alarm.status.value,
            }
        )
        logger.info("before even created")
        event = self._create_event(
            event_type=AlarmEventType.ALARM_TRIGGERED,
            message=f"alarm triggered by sensor {sensor.name} in location {sensor.location}",
            location=sensor.location,
            alarm=alarm,
            user_id=None,
            device_id=None,
        )
        logger.info("after even created")
        self._notify_users(
            title="Alarm triggered",
            message=f"Alarm triggered by sensor {sensor.name} in location {sensor.location}",
            event_id=event.id,
            alarm=alarm,
        )
        self._push_to_users(alarm=alarm)
        logger.info("Triggered before asyncio")
        loop = get_event_loop()
        future = asyncio.run_coroutine_threadsafe(
            self._activation_timer(alarm.id),
            loop,
        )
        future.add_done_callback(
            lambda f: logger.exception(
                "Activation timer failed",
                exc_info=f.exception(),
            ) if f.exception() else None
        )
        logger.info("Triggered after asyncio")

    def _activate_alarm(
        self,
        alarm: Alarm,
    ):

        self.alarm_service.set_alarm_status(
            alarm = alarm,
            alarm_status=AlarmStatus.ACTIVATED,
        )

        self.mqtt_service.publish_alarm_command(
                alarm_id=alarm.id,
                state=AlarmStatus.ACTIVATED,
        )

        self.websocket_service.send_message_sync(
            alarm_id=alarm.id,
            event_type=MessageEventType.ALARM_STATUS_CHANGED,
            data={
                "status": alarm.status.value,
            }
        )
        event = self._create_event(
            event_type=AlarmEventType.ALARM_ACTIVATED,
            message=f"Alarm activated!",
            alarm=alarm,
            user_id=None,
            device_id=None,
            location=None
        )
        self._notify_users(
            title="Alarm activated",
            message="Alarm activated",
            event_id=event.id,
            alarm=alarm,
        )
        logger.info("End activation func")

    def _create_event(
        self,
        event_type: AlarmEventType,
        message: str,
        user_id: int | None,
        device_id: int | None,
        location: str | None,
        alarm:Alarm
    ) -> AlarmEvent:
        request = AlarmEventCreate(
            event_type=event_type,
            message=message,
            user_id=user_id,
            device_id=device_id,
            location=location,
        )
        event = self.alarm_event_service.create(alarm, request)
        return event

    def _notify_users(
        self,
        title: str,
        message: str,
        event_id: int,
        alarm:Alarm,
    ) -> None:
        users = self.user_service.get_users_by_alarm(alarm.id)
        for user in users:
            request = NotificationCreate(
                user_id=user.user_id,
                title=title,
                message=message,
                event_id=event_id,
                notification_type=NotificationType.INFO,
            )
            self.notification_service.create(alarm, request)

    def _push_to_users(
            self,
            alarm:Alarm,
        ) -> None:
            users = self.user_service.get_users_by_alarm(alarm.id)
            for user in users:
                self.push_notification_service.send_to_user(
                    user_id=user.user_id,
                    title="🚨 Alarm",
                    message=f"alarm {alarm.name} triggered",
                    data={
                        "alarm_id": alarm.id,
                        "event": "ALARM_TRIGGERED",
                    },
                )

    def get_alarm_status(self, alarm) -> AlarmStatus:
        return alarm.status
    
    async def _activation_timer(
        self,
        alarm_id: int,
    ):
        logger.info("Start activation timer")
        
        delay = 10
        await asyncio.sleep(delay)
        logger.info("End activation timer")

        alarm = self.alarm_service.get_by_id(alarm_id)

        if alarm.status != AlarmStatus.TRIGGERED:
            return

        self._activate_alarm(alarm)
        logger.info("Alarm activated")