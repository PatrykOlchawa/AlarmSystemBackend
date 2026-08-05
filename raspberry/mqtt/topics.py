class Topics:
    SENSOR = "alarm/+/sensor/#"
    STATE = "alarm/+/state/#"

    @staticmethod
    def command(
        alarm_id: int,
        device: str,
    ) -> str:
        return f"alarm/{alarm_id}/command/{device}"

    @staticmethod
    def sensor(
        alarm_id:int,
        sensor:str,
    ) -> str:
        return f"alarm/{alarm_id}/sensor/{sensor}"

    @staticmethod
    def state(
        alarm_id:int,
        device: str,
    ) -> str:
        return f"alarm/{alarm_id}/state/{device}"