from fastapi import FastAPI
from app.db.database import engine
from app.db.base import Base
from app.modules.users.model import User
import app.db.models
from app.modules.users.router import router as users_router
from app.modules.auth.router import router as auth_router
from app.modules.sensors.router import router as sensor_router
from app.modules.readings.router import router as sensor_reading_router
from app.modules.events.router import router as alarm_event_router
from app.modules.notifications.router import router as notification_router
from app.modules.settings.router import router as settings_router
from app.modules.alarm.router import router as alarm_router
from app.modules.devices.router import router as devices_router
from app.modules.control_devices.router import router as control_devices_router
from app.modules.car_plates.router import router as car_plate_router

from app.core.exception_handlers import register_exception_handlers
from app.security.hashing import password_hasher

import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="AlarmAPI",
    description="REST API for RaspberryPi Alarm System",
    version="1.0.0"
)
register_exception_handlers(app)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(sensor_router)
app.include_router(sensor_reading_router)
app.include_router(alarm_event_router)
app.include_router(notification_router)
app.include_router(settings_router)
app.include_router(alarm_router)
app.include_router(devices_router)
app.include_router(control_devices_router)
app.include_router(car_plate_router)

@app.get("/")
def root():
    return {"message": "Alarm systen API is running"}

#print(password_hasher.hash_password("admin12345"))