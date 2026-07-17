import logging
from app.modules.devices.service import DeviceService
logger = logging.getLogger(__name__)
class DeviceControlService:
    def __init__(
        self,
        device_service: DeviceService,
        ):
        self.device_service = device_service

    def turn_on_led(self, device):
        logger.info(f"Turning on LED for device {device.name}")
    
    def turn_off_led(self, device):
        logger.info(f"Turning off LED for device {device.name}")
        
    def turn_on_buzzer(self, device):
        logger.info(f"Turning on BUZZER for device {device.name}")
    def turn_off_buzzer(self, device):
        logger.info(f"Turning off BUZZER for device {device.name}")
    def move_servo(self, device, angle):
        logger.info(f"Moving servodevice {device.name}, by {angle}")
        
    def move_motor(self, device, direction, steps):
        logger.info(f"Moving motor {device.name}, by {direction}, {steps}")
        
    def turn_on_camera(self, device): 
        logger.info(f"Turning on camera for device {device.name}")
    def turn_off_camera(self, device): 
        logger.info(f"Turning off camera for device {device.name}")