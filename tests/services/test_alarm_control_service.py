from unittest.mock import MagicMock, AsyncMock, patch

from app.common.enums import (
    AlarmStatus,
    MessageEventType,
    SensorType,
)

def test_armed_alarm_is_triggered_by_pir(
    alarm_control_service,
    alarm_service_dependencies,
    alarm,
    pir_sensor,
    sensor_reading,
):
    alarm.status = AlarmStatus.ARMED
    pir_sensor.type = SensorType.PIR

    alarm_service_dependencies[
        "alarm_service"
    ].get_by_id.return_value = alarm

    alarm_service_dependencies[
        "sensor_service"
    ].get_sensor_by_id.return_value = pir_sensor

    alarm_control_service._trigger_alarm = MagicMock()

    alarm_control_service.process_sensor_reading(
        alarm_id=alarm.id,
        reading=sensor_reading,
    )

    alarm_control_service._trigger_alarm.assert_called_once_with(
        alarm=alarm,
        sensor=pir_sensor,
    )

def test_disarmed_alarm_is_triggered_by_pir(
    alarm_control_service,
    alarm_service_dependencies,
    alarm,
    pir_sensor,
    pir_no_motion_reading,        
):
    alarm.status = AlarmStatus.DISARMED
    pir_sensor.type = SensorType.PIR
    alarm_service_dependencies[
        "alarm_service"
    ].get_by_id.return_value = alarm

    alarm_service_dependencies[
        "sensor_service"
    ].get_sensor_by_id.return_value = pir_sensor

    alarm_control_service._trigger_alarm = MagicMock()

    alarm_control_service.process_sensor_reading(
        alarm_id=alarm.id,
        reading=pir_no_motion_reading,
    )

    alarm_control_service._trigger_alarm.assert_not_called()

def test_alarm_sensor_no_exists(
    alarm_control_service,
    alarm_service_dependencies,
    alarm,
    pir_no_motion_reading,         
):
    alarm.status = AlarmStatus.ARMED 

    alarm_service_dependencies[
        "alarm_service"
    ].get_by_id.return_value = alarm

    alarm_service_dependencies[
        "sensor_service"
    ].get_sensor_by_id.return_value = None

    alarm_control_service._trigger_alarm = MagicMock()

    alarm_control_service.process_sensor_reading(
        alarm_id=alarm.id,
        reading=pir_no_motion_reading,
    )

    alarm_control_service._trigger_alarm.assert_not_called()



def test_alarm_no_exists(
    alarm_control_service,
    alarm_service_dependencies,
    alarm,
    pir_no_motion_reading,         
):
    alarm_service_dependencies[
        "alarm_service"
    ].get_by_id.return_value = None

    alarm_control_service._trigger_alarm = MagicMock()

    alarm_control_service.process_sensor_reading(
        alarm_id=alarm.id,
        reading=pir_no_motion_reading,
    )

    alarm_control_service._trigger_alarm.assert_not_called()
    alarm_service_dependencies[
        "sensor_service"
    ].get_sensor_by_id.assert_not_called()

@patch("app.services.alarm_service.get_event_loop")
@patch("app.services.alarm_service.asyncio.run_coroutine_threadsafe")
def test_trigger_alarm(
    mock_run_coroutine_threadsafe,
    mock_get_event_loop,
    alarm_control_service,
    alarm_service_dependencies,
    alarm,
    pir_sensor,  
    event, 
):
    alarm.status = AlarmStatus.ARMED
    alarm_control_service._create_event = MagicMock(
        return_value = event
    )
    alarm_control_service._notify_users = MagicMock()
    alarm_control_service._push_to_users = MagicMock()
    alarm_control_service._activation_timer = AsyncMock()

    mock_loop = MagicMock()
    mock_get_event_loop.return_value = mock_loop

    mock_future = MagicMock()
    mock_run_coroutine_threadsafe.return_value = mock_future

    alarm_control_service._trigger_alarm(
        alarm=alarm,
        sensor=pir_sensor,
    )

    alarm_service_dependencies[
        "alarm_service"
    ].set_alarm_status.assert_called_once_with(
        alarm,
        AlarmStatus.TRIGGERED
    )

    alarm_service_dependencies[
        "mqtt_service"
    ].publish_alarm_command.assert_called_once_with(
        alarm_id=alarm.id,
        state=AlarmStatus.TRIGGERED
    )

    alarm_service_dependencies[
        "websocket_service"
    ].send_message_sync.assert_called_once_with(
        alarm_id=alarm.id,
        event_type=MessageEventType.ALARM_STATUS_CHANGED,
        data={
            "status": alarm.status.value,
        },
    )

    alarm_control_service._create_event.assert_called_once()

    alarm_control_service._notify_users.assert_called_once_with(
        title="Alarm triggered",
        message=f"Alarm triggered by sensor {pir_sensor.name} in location {pir_sensor.location}",
        event_id=event.id,
        alarm=alarm,
    )

    alarm_control_service._push_to_users.assert_called_once_with(alarm=alarm)