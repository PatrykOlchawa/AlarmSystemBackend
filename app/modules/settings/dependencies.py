from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.modules.settings.repository import (
    SettingRepository,
)
from app.modules.settings.service import (
    SettingService,
)

def get_setting_repository(
    db: Session = Depends(get_db),
) -> SettingRepository:

    return SettingRepository(db)

def get_settings_service(
    repository: SettingRepository = Depends(
        get_setting_repository
    ),
) -> SettingService:

    return SettingService(repository)