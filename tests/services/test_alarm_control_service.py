from unittest.mock import MagicMock

from app.common.enums import (
    AlarmStatus,
    MessageEventType,
    SensorType,
)

def test_armed_alarm_is_triggered_by_pir(
    alarm_control_service,
    alarm_service_dependencies,
    armed_alarm,
    pir_sensor,
    sensor_reading
):
    armed_alarm.status = AlarmStatus.ARMED
    pir_sensor.type = SensorType.PIR

    alarm_service_dependencies[
        "alarm_service"
    ].get_by_id.return_value = armed_alarm

    alarm_service_dependencies[
        "sensor_service"
    ].get_sensor_by_id.return_value = pir_sensor

    alarm_control_service._trigger_alarm = MagicMock()

    alarm_control_service.process_sensor_reading(
        alarm_id=armed_alarm.id,
        reading=sensor_reading,
    )

    alarm_control_service._trigger_alarm.assert_called_once_with(
        alarm=armed_alarm,
        sensor=pir_sensor,
    )