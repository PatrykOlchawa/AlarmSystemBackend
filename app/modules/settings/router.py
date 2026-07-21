from urllib import response
from fastapi import APIRouter, Depends, status

from app.modules.settings.dependencies import (
    get_settings_service,
)

from app.modules.settings.schemas import (
    SettingCreate,
    SettingRead,
    SettingUpdate,
)

from app.modules.settings.service import (
    SettingService,
)

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)

@router.get(
    "",
    response_model=list[SettingRead],

)
def get_all_settings(
    service: SettingService = Depends(get_settings_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_all()

@router.get(
    "/{key}",
    response_model=SettingRead,
)
def get_setting(
    key: str,
    service: SettingService = Depends(get_settings_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_by_key(key)

@router.post(
    "",
    response_model=SettingRead,
    status_code=status.HTTP_201_CREATED,
)
def create_setting(
    request: SettingCreate,
    service: SettingService = Depends(get_settings_service),
    current_user: User = Depends(get_current_user),
):
    return service.create(request)

@router.patch(
    "/{key}",
    response_model=SettingRead,
)
def update_setting(
    key: str,
    request: SettingUpdate,
    service: SettingService = Depends(get_settings_service),
    current_user: User = Depends(get_current_user),
):
    return service.update(key, request)

@router.delete(
    "/{key}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_setting(
    key: str,
    service: SettingService = Depends(get_settings_service),
    current_user: User = Depends(get_current_user),
):
    service.delete(key)    