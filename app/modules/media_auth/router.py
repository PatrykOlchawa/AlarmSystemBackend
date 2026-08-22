from fastapi import APIRouter
from app.core.config import settings
from app.modules.media_auth.service import MediaAuthService 
router = APIRouter()

media_auth_service = MediaAuthService(
    private_key_path=settings.mediamtx_private_key_path,
    key_id=settings.mediamtx_key_id,
)

@router.get("/.well-known/jwks.json")
def get_jwks():
    return media_auth_service.get_jwks()