from sqlalchemy.orm import decl_api
import logging
from app.core.exceptions import (
    CarNotAuthorizedException,
    CarPlateNotFoundException,
)

from app.modules.devices.model import Device
from app.modules.devices.service import DeviceService
from app.modules.settings.service import SettingService
from app.modules.car_plates.service import CarPlateService

from app.services.device_control_service import DeviceControlService
from app.services.ocr_service import OCRService
logger = logging.getLogger(__name__)

class TollgateService:
    def __init__(
        self,
        #camera: Device,
        device_control_service: DeviceControlService,
        ocr_service: OCRService,
        car_plate_service: CarPlateService,
        settings_service: SettingService,
        device_service: DeviceService,
    ):
        #self.camera = camera
        self.device_control_service = device_control_service
        self.ocr_service = ocr_service
        self.car_plate_service = car_plate_service
        self.settings_service = settings_service
        self.device_service = device_service

    def process_vehicle(self):
        #image = self.device_control_service.capture_image(self.camera)
        image = "./plate2.png"
        plate = self.ocr_service.read_license_plate(image)
        logger.info(f"Plate: {plate}")

        if plate is None:
            raise CarPlateNotFoundException()
        car_plate = self.car_plate_service.get_by_plate_number(plate)
        logger.info(f"Plate {car_plate} ")
        if car_plate is None:
            raise CarPlateNotFoundException()
        
        if car_plate.auto_open:
            #self.device_control_service.open_gate(self.camera)
            logger.info(f"Plate authorized {car_plate.plate_number}")
        else:
            raise CarNotAuthorizedException()

        return car_plate
