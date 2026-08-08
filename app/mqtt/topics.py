class Topics:
    SENSOR = "alarm/+/sensor/#"
    STATE = "alarm/+/state/#"
    EVENT = "alarm/+/event"
    HEARTBEAT = "alarm/+/heartbeat"

    @staticmethod
    def command_alarm(
        alarm_id: int,
    ) -> str:
        return f"alarm/{alarm_id}/command/alarm"
    
    @staticmethod
    def command_device(
        alarm_id: int,
        device_id: str,
    ) -> str:
        return f"alarm/{alarm_id}/command/device/{device_id}"

    @staticmethod
    def sensor(
        alarm_id:int,
        sensor_id:int,
    ) -> str:
        return f"alarm/{alarm_id}/sensor/reading/{sensor_id}"

    @staticmethod
    def state_alarm(
        alarm_id:int,
    ) -> str:
        return f"alarm/{alarm_id}/state/alarm"

    @staticmethod
    def state_device(
        alarm_id:int,
        device_id: int,
    ) -> str:
        return f"alarm/{alarm_id}/state/device/{device_id}"