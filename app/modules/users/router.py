from fastapi import (
    APIRouter,
    Depends,
    status,
)
from app.modules.users.schema import (
    UserCreate,
    UserResponse,
    AlarmMemberResponse,
    UserUpdate,
    ChangePassword,
)

from app.security.auth_dependencies import get_current_user
from app.modules.users.model import User
from app.modules.users.service import UserService
from app.modules.users.dependencies import get_user_service
from app.security.authorization_dependencies import require_alarm_admin

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    response_model=list[UserResponse],
)
def get_users(
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_all_users()

@router.get(
    "/alarm/{alarm_id}",
    response_model=list[AlarmMemberResponse]
)
def get_users_by_alarm(
    alarm_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_users_by_alarm(alarm_id)

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_user_by_id(user_id)


@router.post(
    "/",
    response_model=UserResponse
)
def create (
    request: UserCreate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return service.create(request)

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    service.delete(user_id)

@router.patch(
    "/change_password",
    response_model=UserResponse,
)
def change_password(
    request: ChangePassword,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    user = service.change_password(current_user, request)
    return user

@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
def update(
    user_id: int,
    request: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return service.update(user_id, request)

