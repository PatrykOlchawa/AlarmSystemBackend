from raspberry.mqtt.publishers.state_publisher import StatePublisher
class DeviceControlService:
    def __init__(
        self,
        state_publisher: StatePublisher
    ):

        pass
    def execute(
        self,
        alarm_id: int,
        device_name: str,
        payload: str,
    ):
        pass