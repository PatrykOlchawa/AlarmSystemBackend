from app.modules.alarms.model import Alarm
from app.common.enums import ConnectionType
from app.common.enums import DeviceType
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.devices.model import Device


class DeviceRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def get_all(self, alarm:Alarm) -> list[Device]:
        stmt = (
            select(Device)
            .where(Device.alarm_id == alarm.id)
            .order_by(Device.name)
        )
        return list(self.session.scalars(stmt))
    
    def get_by_id(
        self,
        alarm:Alarm,
        device_id: int
    ) -> Device | None:
        stmt = (
            select(Device)
            .where(Device.id == device_id)
            .where(Device.alarm_id == alarm.id)
        )
        return self.session.scalar(stmt)
    
    def get_by_name(
        self,
        alarm:Alarm,
        name: str
    ) -> Device | None:
        stmt = (
            select(Device)
            .where(Device.name == name)
            .where(Device.alarm_id == alarm.id)
        )
        return self.session.scalar(stmt)
    
    def create(
        self,
        alarm:Alarm,
        device: Device
    ) -> Device:
        self.session.add(device)
        self.session.commit()
        self.session.refresh(device)
        return device
    
    def update(
        self,
        alarm:Alarm,
        device: Device
    ) -> Device:        
        self.session.commit()
        self.session.refresh(device)
        return device

    def delete(
        self,
        alarm:Alarm,
        device: Device
    ) -> None:
        self.session.delete(device)
        self.session.commit()

    def get_by_type(
        self,
        alarm:Alarm,
        device_type: DeviceType
    ) -> list[Device]:
        stmt = (
            select(Device)
            .where(Device.alarm_id == alarm.id)
            .where(Device.type == device_type)

        )
        return list(self.session.scalars(stmt))

    def get_by_connection_type(
        self,
        alarm:Alarm,
        connection_type: ConnectionType
    ) -> list[Device]:
        stmt = (
            select(Device)
            .where(Device.connection_type == connection_type)
            .where(Device.alarm_id == alarm.id)
        )
        return list(self.session.scalars(stmt))

    def get_enabled_devices(
        self,
        alarm:Alarm
    ) -> list[Device]:
        stmt = (
            select(Device)
            .where(Device.enabled == True)
            .where(Device.alarm_id == alarm.id)
        )
        return list(self.session.scalars(stmt))
        
    