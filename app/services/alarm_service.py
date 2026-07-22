from app.modules.alarms.model import Alarm
from app.services.tollgate_service import TollgateService
from app.services import tollgate_service
from app.modules.devices.service import DeviceService
from app.common.enums import DeviceType
from app.services.device_control_service import DeviceControlService
from app.core.exceptions import InvalidPinException
from app.modules.auth.service import AuthService
from app.core.exceptions import AlarmAlreadyDisarmedException
from app.core.exceptions import InvalidAlarmStateException
from app.modules.notifications.schemas import NotificationCreate
from app.common.enums import NotificationType
from app.modules.events.model import AlarmEvent
from app.common.enums import AlarmStatus
from app.modules.sensors.model import Sensor
from app.common.enums import AlarmEventType,SensorType
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
    
    def process_sensor_reading(
        self,
        reading: SensorReading,
    ) -> None:
        

        sensor = self.sensor_service.get_sensor_by_id(reading.sensor_id)
        if sensor is None:
            return
        alarm = sensor.alarm
        if alarm.status != AlarmStatus.ARMED:
            return
        
        match sensor.sensor_type:
            case SensorType.PIR:
                self._process_motion(sensor, reading)
            case SensorType.HUMIDITY:
                self._process_door(sensor, reading)
            case SensorType.TEMPERATURE:
                self._process_temperature(sensor, reading)
            case SensorType.LDR:
                self._process_ldr(sensor, reading)
            case SensorType.DHT11:
                self._process_dht11(sensor, reading)
        

    def arm_alarm(
        self,
        alarm: Alarm,
        user_id:int,
        pin:str,
    ) -> None:
        user = self.user_service.get_user_by_id(user_id)
        if not password_hasher.verify_pin(pin,user.pin_hash):
            raise InvalidPinException()
        alarm_status = alarm.status
        if alarm_status!= AlarmStatus.DISARMED:
            raise InvalidAlarmStateException(alarm_status)

        self.alarm_service.set_alarm_status(alarm, AlarmStatus.ARMING)
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
        
        #self.tollgate_service.process_vehicle()
    
    def disarm_alarm(
        self,
        alarm: Alarm,
        user_id:int,
        pin:str,
    ) -> None:
        user = self.user_service.get_user_by_id(user_id)
        if not password_hasher.verify_pin(pin,user.pin_hash):
            raise InvalidPinException()
            
        if alarm.status == AlarmStatus.DISARMED:
            raise AlarmAlreadyDisarmedException()
        
        self._deactivate_alarm_devices(alarm)
        self.alarm_service.set_alarm_status(alarm, AlarmStatus.DISARMED)

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
    
    def _trigger_alarm(
        self,
        title: str,
        event_type: AlarmEventType,
        message: str,
        user_id: int | None,
        device_id: int | None,
        location: str | None,
        alarm: Alarm

    ) -> None:

        if alarm.status == AlarmStatus.TRIGGERED:
            return
        
        self.settings_service.set_alarm_status(alarm, AlarmStatus.TRIGGERED)
        event = self._create_event(
            event_type=event_type,
            message=message,
            user_id=user_id,
            device_id=device_id,
            location=location,
            alarm=alarm
        )
        self._notify_users(
            title=title,
            message=message,
            event_id=event.id,
            alarm=alarm,
        )
    
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
                user_id=user.id,
                title=title,
                message=message,
                event_id=event_id,
                notification_type=NotificationType.INFO,
            )
            self.notification_service.create(alarm, request)
    
    def get_alarm_status(self, alarm) -> AlarmStatus:
        return alarm.status
    
    def _activate_alarm_devices(self, alarm):
        leds = self.device_service.get_by_type(alarm, DeviceType.LED)
        for led in leds:
            self.device_control_service.turn_on_led(led)
        buzzer = self.device_service.get_by_type(alarm, DeviceType.BUZZER)
        for buzzer in buzzer:
            self.device_control_service.turn_on_buzzer(buzzer)
        servos = self.device_service.get_by_type(alarm, DeviceType.SERVO)
        for servo in servos:
            self.device_control_service.move_servo(servo,180)
        motors = self.device_service.get_by_type(alarm, DeviceType.MOTOR)
        for motor in motors:
            self.device_control_service.move_motor(motor,'LEFT',100)
        cameras = self.device_service.get_by_type(alarm, DeviceType.CAMERA)
        for camera in cameras:
            self.device_control_service.turn_on_camera(camera)

    def _deactivate_alarm_devices(self, alarm):
        leds = self.device_service.get_by_type(alarm, DeviceType.LED)
        for led in leds:
            self.device_control_service.turn_off_led(led)
        buzzer = self.device_service.get_by_type(alarm, DeviceType.BUZZER)
        for buzzer in buzzer:
            self.device_control_service.turn_off_buzzer(buzzer)
        servos = self.device_service.get_by_type(alarm, DeviceType.SERVO)
        for servo in servos:
            self.device_control_service.move_servo(servo,0)
        motors = self.device_service.get_by_type(alarm, DeviceType.MOTOR)
        for motor in motors:
            self.device_control_service.move_motor(motor,'RIGHT',100)
        cameras = self.device_service.get_by_type(alarm, DeviceType.CAMERA)
        for camera in cameras:
            self.device_control_service.turn_off_camera(camera)