from app.core.config import settings
from app.modules.media_auth.service import MediaAuthService

def get_media_auth_service() -> MediaAuthService:
    return MediaAuthService(
        private_key_path=settings.mediamtx_private_key_path,
        key_id=settings.mediamtx_key_id,
    )
