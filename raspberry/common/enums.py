from enum import Enum

class AlarmStatus(str, Enum):
    ARMED = "ARMED"
    DISARMED = "DISARMED"
    TRIGGERED = "TRIGGERED"
    ARMING = "ARMING"
    DISARMING = "DISARMING"
    UNKNOWN = "UNKNOWN"   
    ACTIVATED = "ACTIVATED" 

class DeviceType(str, Enum):
    SENSOR = "SENSOR"
    MOTOR = "MOTOR"
    RGB_LED = "RGB_LED"
    BUZZER = "BUZZER"
    LED = "LED"
    LCD = "LCD"
    CAMERA = "CAMERA"
    SERVO = "SERVO"

class SensorType(str, Enum):
    LDR = "LDR"
    DHT11 = "DHT11"
    PIR = "PIR"
    TEMPERATURE = "TEMPERATURE"
    HUMIDITY = "HUMIDITY"

class MQTTMessageType(str, Enum):
    SENSOR = "sensor"
    STATE = "state"
    COMMAND = "command"
    EVENT = "event"
    HEARTBEAT = "heartbeat"