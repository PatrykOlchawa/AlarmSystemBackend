from app.modules.devices.service import DeviceService
from app.security.authorization_dependencies import require_alarm_admin
from app.modules.alarms.model import Alarm
from app.common.schemas import MessageResponse
from app.modules.alarm.schemas import AlarmMessageResponse
from app.modules.devices.model import Device
from app.common.enums import DeviceType
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.dependencies import  get_device_control_service
from app.modules.devices.dependencies import get_device_service
from app.services.device_control_service import DeviceControlService
from app.modules.users.model import User
from app.security.auth_dependencies import get_current_user
router = APIRouter(
    prefix="/alarms/{alarm_id}/control-devices",
    tags=["Control Devices"],
)

def _get_device_or_raise(
    device_id: int,
    expected_type: DeviceType,
    service : DeviceService = Depends(get_device_service),
    alarm : Alarm = Depends(require_alarm_admin),   
) -> Device:
    device = service.get_by_id(alarm, device_id)
    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found",
        )
    if device.type != expected_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Device is not of type {expected_type.value}",
        )
    return device

@router.post(
    "led/{device_id}/on",
    response_model=MessageResponse,
    )
def turn_on_led(
    device_id: int,
    alarm : Alarm = Depends(require_alarm_admin),
    device_service = Depends(get_device_service),
    control_service = Depends(get_device_control_service),
) -> AlarmMessageResponse:
    device = _get_device_or_raise(
        device_id,
        DeviceType.LED,
        device_service,
        alarm,
    )
    control_service.turn_on_led(device)
    return MessageResponse(
        message="LED turned on",
    )
@router.post(
    "/led/{device_id}/off",
    response_model=MessageResponse,
    )
def turn_off_led(
    device_id: int,
    alarm : Alarm = Depends(require_alarm_admin),
    device_service = Depends(get_device_service),
    control_service = Depends(get_device_control_service),
) -> MessageResponse:
    device = _get_device_or_raise(
        device_id,
        DeviceType.LED,
        device_service,
        alarm,
    )
    control_service.turn_off_led(device)
    return MessageResponse(
        message="LED turned on",
    )

@router.post(
    "/buzzer/{device_id}/on",
    response_model=MessageResponse,
    )
def turn_on_buzzer(
    device_id: int,
    alarm : Alarm = Depends(require_alarm_admin),
    device_service = Depends(get_device_service),
    control_service = Depends(get_device_control_service),
) -> MessageResponse:
    device = _get_device_or_raise(
        device_id,
        DeviceType.BUZZER,
        device_service,
        alarm,
    )
    control_service.turn_on_buzzer(device)
    return MessageResponse(
        message="Buzzer turned on",
    )

@router.post(
    "/buzzer/{device_id}/off",
    response_model=MessageResponse,
    )
def turn_off_buzzer(
    device_id: int,
    alarm : Alarm = Depends(require_alarm_admin),
    device_service = Depends(get_device_service),
    control_service = Depends(get_device_control_service),
) -> MessageResponse:
    device = _get_device_or_raise(
        device_id,
        DeviceType.BUZZER,
        device_service,
        alarm,
    )
    control_service.turn_off_buzzer(device)
    return MessageResponse(
        message="Buzzer turned off",
    )

@router.post(
    "/camera/{device_id}/on",
    response_model=MessageResponse,
    )
def turn_on_camera(
    device_id: int,
    alarm : Alarm = Depends(require_alarm_admin),   
    device_service = Depends(get_device_service),
    control_service = Depends(get_device_control_service),
) -> MessageResponse:
    device = _get_device_or_raise(
        device_id,
        DeviceType.CAMERA,
        device_service,
        alarm,
    )
    control_service.turn_on_camera(device)
    return MessageResponse(
        message="Camera turned on",
    )

@router.post(
    "/camera/{device_id}/off",
    response_model=MessageResponse,
    )
def turn_off_camera(
    device_id: int,
    alarm : Alarm = Depends(require_alarm_admin),
    device_service = Depends(get_device_service),
    control_service = Depends(get_device_control_service),
) -> MessageResponse:
    device = _get_device_or_raise(
        device_id,
        DeviceType.CAMERA,
        device_service,
        alarm,
    )
    control_service.turn_off_camera(device)
    return MessageResponse(
        message="Camera turned off",
    )

@router.post(
    "/servo/{device_id}/move",
    response_model=MessageResponse,
    )
def move_servo(
    device_id: int,
    angle: int,
    alarm : Alarm = Depends(require_alarm_admin),   
    device_service = Depends(get_device_service),
    control_service = Depends(get_device_control_service),
) -> MessageResponse:
    device = _get_device_or_raise(
        device_id,
        DeviceType.SERVO,
        device_service,
        alarm,
    )
    control_service.move_servo(device, angle)
    return MessageResponse(
        message=f"Servo moved by {angle} degrees",
    )

@router.post(
    "/motor/{device_id}/move",
    response_model=MessageResponse,
    )
def move_motor(
    device_id: int,
    direction: str,
    steps: int,
    alarm : Alarm = Depends(require_alarm_admin),   
    device_service = Depends(get_device_service),
    control_service = Depends(get_device_control_service),
) -> MessageResponse:
    device = _get_device_or_raise(
        device_id,
        DeviceType.MOTOR,
        device_service,
        alarm,
    )
    control_service.move_motor(device, direction, steps)
    return MessageResponse(
        message=f"Motor moved to {direction} by {steps} steps",
    )
    