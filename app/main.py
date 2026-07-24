from fastapi import FastAPI
from app.db.database import engine
from app.db.base import Base
from app.modules.users.model import User
import app.db.models
from app.modules.users.router import router as users_router

from app.modules.auth.router import router as auth_router
from app.modules.alarm.router import router as alarm_control_router
from app.modules.sensors.router import router as sensor_router
from app.modules.readings.router import router as sensor_reading_router
from app.modules.events.router import router as alarm_event_router
from app.modules.notifications.router import router as notification_router
from app.modules.settings.router import router as settings_router
from app.modules.devices.router import router as devices_router
from app.modules.control_devices.router import router as control_devices_router
from app.modules.car_plates.router import router as car_plate_router
from app.modules.alarms.router import router as alarms_router
from app.core.exception_handlers import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware
import logging
logging.basicConfig(level=logging.INFO)
from fastapicap import Cap

app = FastAPI(
    title="AlarmAPI",
    description="REST API for RaspberryPi Alarm System",
    version="1.0.0"
)

Cap.init_app("redis://redis:6379/0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "https://app.wsb-alarm.pl",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Retry-After"],
)

register_exception_handlers(app)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(sensor_router)
app.include_router(sensor_reading_router)
app.include_router(alarm_event_router)
app.include_router(notification_router)
app.include_router(settings_router)
app.include_router(alarm_control_router)
app.include_router(devices_router)
app.include_router(control_devices_router)
app.include_router(car_plate_router)
app.include_router(alarms_router)

@app.get("/")
def root():
    return {"message": "Alarm systen API is running"}
