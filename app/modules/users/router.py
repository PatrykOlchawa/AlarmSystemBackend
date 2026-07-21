from app.modules.users.schema import UserUpdate
from fastapi import status
from app.security.auth_dependencies import get_current_user
from app.modules.users.model import User
from fastapi import APIRouter
from fastapi import Depends

from app.modules.users.schema import UserCreate
from app.modules.users.schema import UserResponse

from app.modules.users.service import UserService
from app.modules.users.dependencies import get_user_service
from app.modules.alarms.model import Alarm
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
    response_model=list[UserResponse]
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
def create_user(
    request: UserCreate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return service.create_user(request)

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    service.delete_user(user_id)

@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    request: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return service.update_user(user_id, request)