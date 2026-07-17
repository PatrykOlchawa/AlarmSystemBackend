from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    SERVICE = "SERVICE"

class AlarmStatus(str, Enum):
    ARMED = "ARMED"
    DISARMED = "DISARMED"
    TRIGGERED = "TRIGGERED"
    ARMING = "ARMING"
    DISARMING = "DISARMING"
    UNKNOWN = "UNKNOWN"    

class SensorStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    UNKNOWN = "UNKNOWN"

class SensorType(str, Enum):
    LDR = "LDR"
    DHT11 = "DHT11"
    PIR = "PIR"
    TEMPERATURE = "TEMPERATURE"
    HUMIDITY = "HUMIDITY"

class DeviceType(str, Enum):
    SENSOR = "SENSOR"
    MOTOR = "MOTOR"
    RGB_LED = "RGB_LED"
    BUZZER = "BUZZER"
    LED = "LED"
    LCD = "LCD"
    CAMERA = "CAMERA"
    SERVO = "SERVO"

class ConnectionType(str, Enum):
    GPIO = "GPIO"
    I2C = "I2C"
    SPI = "SPI"
    USB = "USB"
    ETHERNET = "ETHERNET"
    WIFI = "WIFI"
    CSI = "CSI"

class AlarmEventType(str, Enum):
    ALARM_ARMED = "ALARM_ARMED"
    ALARM_DISARMED = "ALARM_DISARMED"
    ALARM_TRIGGERED = "ALARM_TRIGGERED"
    ALARM_ARMING = "ALARM_ARMING"
    MOTION_DETECTED = "MOTION_DETECTED"
    TEMPERATURE_TRESHOLD = "TEMPERATURE_TRESHOLD"
    HUMIDITY_TRESHOLD = "HUMIDITY_TRESHOLD"
    CAMERA_MOTION = "CAMERA_MOTION"
    SYSTEM_ERROR = "SYSTEM_ERROR"
    DOOR_OPENED = "DOOR_OPENED"
    DOOR_CLOSED = "DOOR_CLOSED"
    GATE_OPENED = "GATE_OPENED"
    GATE_CLOSED = "GATE_CLOSED"


class NotificationType(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    ALERT = "ALERT"
    SYSTEM = "SYSTEM"

class MotorDirection(str, Enum):
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"