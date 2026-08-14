from fastapi import (    
   APIRouter,
    Depends,
    status,
)
from app.modules.push_tokens.schemas import (
    PushTokenRequest,
    PushTokenResponse,
)
from app.modules.push_tokens.service import PushTokenService
from app.modules.push_tokens.dependencies import get_push_token_service
from app.security.auth_dependencies import get_current_user
from app.modules.users.model import User
router = APIRouter(
    prefix="/users/me/push_tokens",
    tags=["PushToken"]
)


@router.post(
    "/",
    response_model=PushTokenResponse
)
def create(
    request: PushTokenRequest,
    service: PushTokenService = Depends(get_push_token_service),
    current_user: User = Depends(get_current_user),
):
    return service.create(current_user.id, request)

@router.delete(
    "/{push_token_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    push_token_id: int,
    service: PushTokenService = Depends(get_push_token_service),
    current_user: User = Depends(get_current_user),
):
    service.delete(push_token_id, current_user.id)

