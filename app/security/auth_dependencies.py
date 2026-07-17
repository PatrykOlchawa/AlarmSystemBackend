from app.modules.users.repository import UserRepository
from app.modules.users import repository
from jose import JWTError
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from app.modules.auth.schemas import TokenPayload
from app.security.jwt_handler import jwt_handler
from app.modules.users.dependencies import get_user_service
from app.modules.users.service import UserService
from app.common.enums import UserRole
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
)

def get_token_payload(
    token: str = Depends(oauth2_scheme),
) -> TokenPayload:

    try:
        payload = jwt_handler.decode_access_token(token)
        return TokenPayload(**payload)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )
def get_current_user(
    payload: TokenPayload = Depends(get_token_payload),
    repository: UserRepository = Depends(get_user_service),
):
    user = repository.get_user_by_id(payload.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not active",
        )
    return user
def require_admin(
    current = Depends(get_current_user),
):
    if current.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required:"
        )
    return current
