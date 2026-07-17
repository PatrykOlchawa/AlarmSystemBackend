from app.common.schemas import MessageResponse
from app.modules.alarm.schemas import AlarmMessageResponse
from app.modules.devices.model import Device
from app.common.enums import DeviceType
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.devices.service import DeviceService
from app.services.dependencies import get_device_service, get_device_control_service
from app.services.device_control_service import DeviceControlService
from app.modules.users.model import User
from app.security.auth_dependencies import get_current_user
router = APIRouter(
    prefix="/control-devices",
    tags=["Control Devices"],
)

def _get_device_or_raise(
    device_id: int,
    expected_type: DeviceType,
    service: DeviceService,
) -> Device:
    device = service.get_by_id(device_id)
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
    current_user: User = Depends(get_current_user),
    device_service: DeviceService = Depends(get_device_service),
    control_service: DeviceControlService = Depends(get_device_control_service),
) -> AlarmMessageResponse:
    device = _get_device_or_raise(
        device_id,
        DeviceType.LED,
        device_service,
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
    current_user: User = Depends(get_current_user),
    device_service: DeviceService = Depends(get_device_service),
    control_service: DeviceControlService = Depends(get_device_control_service),
) -> MessageResponse:
    device = _get_device_or_raise(
        device_id,
        DeviceType.LED,
        device_service,
    )
    control_service.turn_off_led(device)
    return MessageResponse(
        message="LED turned on",
    )