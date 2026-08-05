from fastapi import (
    APIRouter,
    Depends,
    status,
)
from app.modules.clients.schemas import (
    ClientLoginRequest,
    ClientLoginResponse,
    ClientResponse,
)
from app.modules.auth.service import ClientAuthService
from app.modules.auth.dependencies import get_client_auth_service
from app.security.auth_dependencies import get_current_client
from app.modules.clients.model import Client

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

@router.post(
    "/login",
    response_model=ClientLoginResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    request: ClientLoginRequest,
    service: ClientAuthService = Depends(get_client_auth_service),
):
    return service.login(
        request.client_id,
        request.secret,
    )

@router.get(
    "/me",
    response_model=ClientResponse,
)
def login(
    client: Client = Depends(get_current_client)
):
    return client