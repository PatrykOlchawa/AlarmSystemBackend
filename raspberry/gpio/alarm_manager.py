from common.enums import AlarmStatus

class AlarmManager:
    def __init__(self):
        self._status = AlarmStatus.DISARMED

    @property
    def status(self) -> AlarmStatus:
        return self._status

    def arm(self) -> None:
        self._status = AlarmStatus.ARMED

    def disarm(self) -> None:
        self._status = AlarmStatus.DISARMED

    def trigger(self) -> None:
        self._status = AlarmStatus.TRIGGERED

    def is_armed(self) -> bool:
        return self._status == AlarmStatus.ARMED
    def set_status(
        self,
        status: AlarmStatus,
    ) -> None:
        self._status = status