from app.common.enums import AlarmRole
from fastapi import Depends

from app.modules.alarms.dependencies import get_alarm_service
from app.modules.alarms.model import Alarm
from app.modules.alarms.service import AlarmService
from app.modules.users.model import User
from app.security.auth_dependencies import get_current_user


def require_alarm_member(
    alarm_id: int,
    current_user: User = Depends(get_current_user),
    alarm_service: AlarmService = Depends(get_alarm_service),
) -> Alarm:
    """
    Returns the alarm if the current user is a member of it.
    Raises an exception otherwise.
    """

    return alarm_service.verify_alarm_access(
        alarm_id=alarm_id,
        current_user=current_user,
        required_role={
            AlarmRole.USER,
            AlarmRole.OWNER,
            AlarmRole.ADMIN,
        },
    )

def require_alarm_admin(
    alarm_id: int,
    current_user: User = Depends(get_current_user),
    alarm_service: AlarmService = Depends(get_alarm_service),
) -> Alarm:
    return alarm_service.verify_alarm_access(
        alarm_id=alarm_id,
        current_user=current_user,
        required_role={
            AlarmRole.ADMIN,
            AlarmRole.OWNER,
        },
    )

def require_alarm_owner(
    alarm_id: int,
    current_user: User = Depends(get_current_user),
    alarm_service: AlarmService = Depends(get_alarm_service),
) -> Alarm:
    return alarm_service.verify_alarm_access(
        alarm_id=alarm_id,
        current_user=current_user,
        required_role={
            AlarmRole.OWNER,
        },
    )