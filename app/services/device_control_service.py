from app.modules.devices.model import Device
from app.core.exceptions import InvalidDeviceTypeException
from app.common.enums import DeviceType
from app.services.ocr_service import OCRService
import logging
from app.modules.devices.service import DeviceService
from app.mqtt.service import MQTTService
logger = logging.getLogger(__name__)
class DeviceControlService:
    def __init__(
        self,
        device_service: DeviceService,
        mqtt_service: MQTTService,
    ):
        self.device_service = device_service
        self.mqtt_service = mqtt_service
    def turn_on_led(self, device):
        logger.info(f"Turning on LED for device {device.name}")
        self.mqtt_service.publish_device_command(
            alarm_id=device.alarm_id,
            device_id=device.id,
            payload={
                "state": True,
            },
        )

    def turn_off_led(self, device):
        logger.info(f"Turning off LED for device {device.name}")
        self.mqtt_service.publish_device_command(
            alarm_id=device.alarm_id,
            device_id=device.id,
            payload={
                "state": False,
            },
        )
        
    def turn_on_buzzer(self, device):
        logger.info(f"Turning on BUZZER for device {device.name}")
        self.mqtt_service.publish_device_command(
            alarm_id=device.alarm_id,
            device_id=device.id,
            payload={
                "state": True,
            },
        )
    def turn_off_buzzer(self, device):
        logger.info(f"Turning off BUZZER for device {device.name}")
        self.mqtt_service.publish_device_command(
            alarm_id=device.alarm_id,
            device_id=device.id,
            payload={
                "state": False,
            },
        )
    def move_servo(self, device, angle):
        logger.info(f"Moving servodevice {device.name}, by {angle}")
        self.mqtt_service.publish_device_command(
            alarm_id=device.alarm_id,
            device_id=device.id,
            payload={
                "angle": angle,
            },
        )    
    def move_motor(self, device, direction, steps):
        logger.info(f"Moving motor {device.name}, by {direction}, {steps}")
        self.mqtt_service.publish_device_command(
            alarm_id=device.alarm_id,
            device_id=device.id,
            payload={
                "direction": direction,
                "steps": steps
            },
        )
    def turn_on_camera(self, device): 
        logger.info(f"Turning on camera for device {device.name}")
        self.mqtt_service.publish_device_command(
            alarm_id=device.alarm_id,
            device_id=device.id,
            payload={
                "state": True,
            },
        )
    def turn_off_camera(self, device): 
        logger.info(f"Turning off camera for device {device.name}")
        self.mqtt_service.publish_device_command(
            alarm_id=device.alarm_id,
            device_id=device.id,
            payload={
                "state": False,
            },
        )
    def capture_image(self, device): 
        if device.type != DeviceType.CAMERA:
            raise InvalidDeviceTypeException()
        logger.info(f"Capturing image from device {device.name}")
        
    def open_tollgate(self, devices: list[Device]): 
        for device in devices:    
            if device.type != DeviceType.SERVO:
                raise InvalidDeviceTypeException()
            self.move_servo(device, 90)
        logger.info(f"Opening tollgate")
    
    def close_tollgate(self, devices: list[Device]): 
        for device in devices:
            if device.type != DeviceType.SERVO:
                raise InvalidDeviceTypeException()
            self.move_servo(device, 0)
        logger.info(f"Closing tollgate")