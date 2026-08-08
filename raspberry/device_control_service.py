from raspberry.mqtt.publishers.alarm_state_publisher import AlarmStatePublisher
class DeviceControlService:
    def __init__(
        self,
        state_publisher: AlarmStatePublisher
    ):

        pass
    def execute(
        self,
        alarm_id: int,
        device_name: str,
        payload: str,
    ):
        pass