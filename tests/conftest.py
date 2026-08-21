import pytest
from types import SimpleNamespace
from unittest.mock import MagicMock
from app.services.alarm_service import AlarmControlService

@pytest.fixture
def alarm_service_dependencies():
    return {
        "settings_service": MagicMock(),
        "sensor_service": MagicMock(),
        "alarm_event_service": MagicMock(),
        "notification_service": MagicMock(),
        "user_service": MagicMock(),
        "auth_service": MagicMock(),
        "device_service": MagicMock(),
        "device_control_service": MagicMock(),
        "tollgate_service": MagicMock(),
        "alarm_service": MagicMock(),
        "websocket_service": MagicMock(),
        "user_alarm_repository": MagicMock(),
        "mqtt_service": MagicMock(),
        "push_notification_service": MagicMock(),
    }

@pytest.fixture
def alarm_control_service(alarm_service_dependencies):
    return AlarmControlService(
        **alarm_service_dependencies
    )

@pytest.fixture
def armed_alarm():
    return SimpleNamespace(
        id=1,
        name="Test Alarm",
        status=None,
    )

@pytest.fixture
def pir_sensor():
    return SimpleNamespace(
        id=1,
        name="pir1",
        type=None,
        threshold=None,
        gpio_pin=10,
        location="entrance",
    )

@pytest.fixture
def sensor_reading():
    return SimpleNamespace(
        id=1,
        sensor_reading=1,
        value=1,
        timestamp=None,
        sensor=None
    )