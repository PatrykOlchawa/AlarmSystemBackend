from app.modules.users.model import User
from app.modules.users.schema import UserResponse
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Request
from app.modules.auth.dependencies import (
    get_auth_service,    
)
from app.security.auth_dependencies import (
    get_current_user,
)
from app.modules.auth.schemas import (
    LoginRequest,
    TokenResponse,
)
from app.modules.auth.service import AuthService
from app.core.limiter import limiter



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.get("/me", response_model=UserResponse)
def me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.post(
    "/login",
    response_model=TokenResponse,
)
#@limiter.limit("5/minute")
def login(
    request: Request,
    login_request: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):

    token = service.login(
        login_request.username,
        login_request.password,
    )

    return TokenResponse(
        access_token=token,
    )
#login for Swagger UI
@router.post("/token", response_model=TokenResponse)
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    token = service.login(
        form_data.username,
        form_data.password,
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )