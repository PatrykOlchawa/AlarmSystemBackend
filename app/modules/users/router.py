from app.security.auth_dependencies import get_current_user
from app.modules.users.model import User
from fastapi import APIRouter
from fastapi import Depends

from app.modules.users.schema import UserCreate
from app.modules.users.schema import UserResponse

from app.modules.users.service import UserService
from app.modules.users.dependencies import get_user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=list[UserResponse])
def get_users(
    service: UserService = Depends(get_user_service)
):
    return service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return service.get_user_by_id(user_id)


@router.post("/", response_model=UserResponse)
def create_user(
    request: UserCreate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return service.create_user(
        username=request.username,
        password=request.password,
        pin=request.pin,
    )