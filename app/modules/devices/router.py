from app.modules.users.model import User
from app.security.auth_dependencies import get_current_user
from sqlalchemy.sql.functions import current_user
from fastapi import status
from fastapi import Depends
from app.modules.devices.service import DeviceService
from app.modules.devices.dependencies import get_device_service
from app.modules.devices.schemas import (
    DeviceResponse,
    CameraStreamTokenResponse,
    DeviceUpdate,
    DeviceCreate,
    CameraStreamResponse,
) 
from fastapi import APIRouter
from app.modules.alarms.model import Alarm
from app.security.authorization_dependencies import require_alarm_admin
from app.security.authorization_dependencies import require_alarm_member
from app.modules.media_auth.service import MediaAuthService
from app.modules.media_auth.dependencies import get_media_auth_service
from app.common.enums import DeviceType
from app.core.config import settings
router = APIRouter(
    prefix="/alarms/{alarm_id}/devices",
    tags=["Devices"],
)

@router.get(
    "",
    response_model=list[DeviceResponse],
)
def get_devices(
    service: DeviceService = Depends(get_device_service),
    alarm : Alarm = Depends(require_alarm_member),
):
    return service.get_all(alarm)

@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
)
def get_device(
    device_id: int,
    service: DeviceService = Depends(get_device_service),
    alarm : Alarm = Depends(require_alarm_member),
):
    return service.get_by_id(alarm,device_id)

@router.get(
    "/cameras/stream-token",
    response_model=CameraStreamTokenResponse,
)
def get_camera_stream_token(
    alarm : Alarm = Depends(require_alarm_member),
    current_user: User = Depends(get_current_user),
    devices_service: DeviceService = Depends(get_device_service),
    media_auth_service: MediaAuthService = Depends(get_media_auth_service),
):
    cameras = devices_service.get_by_type(
        alarm=alarm,
        device_type=DeviceType.CAMERA
    )
    permissions = media_auth_service.create_camera_permissions(
        alarm = alarm,
        cameras = cameras,
    )

    token = media_auth_service.create_camera_stream_token(
        permissions=permissions
    )

    return CameraStreamTokenResponse(
        token=token,
        expires_in=settings.mediamtx_token_expire_minutes * 60,
        cameras=[
            CameraStreamResponse(
                device_id=camera.id,
                connection_identifier=camera.connection_identifier,
                path=media_auth_service.get_camera_path(
                    alarm=alarm,
                    camera=camera,
                ),
            )
            for camera in cameras
        ],
    )

@router.post(
    "",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_device(
    request: DeviceCreate,
    service: DeviceService = Depends(get_device_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.create(alarm,request)

@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
)
def update_device(
    device_id: int,
    request: DeviceUpdate,
    service: DeviceService = Depends(get_device_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.update(alarm,device_id, request)

@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_device(
    device_id: int,
    service: DeviceService = Depends(get_device_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    service.delete(alarm,device_id)
