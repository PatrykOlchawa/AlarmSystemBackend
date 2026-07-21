from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.devices.repository import DeviceRepository
from app.modules.devices.service import DeviceService


def get_device_repository(
    db: Session = Depends(get_db),
) -> DeviceRepository:
    return DeviceRepository(db)


def get_device_service(
    repository: DeviceRepository = Depends(get_device_repository),
) -> DeviceService:
    return DeviceService(repository)