from fastapi import (
    APIRouter,
    Depends,
    status,
)
from app.modules.clients.schemas import (
    ClientLoginRequest,
    ClientLoginResponse,
    ClientResponse,
    ConfigResponse,
)
from app.modules.auth.service import ClientAuthService
from app.modules.auth.dependencies import get_client_auth_service
from app.security.auth_dependencies import get_current_client
from app.services.dependencies import get_config_service
from app.modules.clients.model import Client
from app.modules.clients.service import ClientService
from app.services.config_service import ConfigService

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

@router.get(
    "/config",
    response_model=ConfigResponse,
)
def config(
    client: Client = Depends(get_current_client),
    service: ConfigService = Depends(get_config_service),
):
    return service.get_config(client)