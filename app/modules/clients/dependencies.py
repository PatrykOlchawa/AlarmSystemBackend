from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.db.session import get_db
from app.modules.clients.repository import ClientRepository
from app.modules.clients.service import ClientService

def get_client_repository(
    db: Session = Depends(get_db)
):
    return ClientRepository(db)

def get_client_service(
    repository: ClientRepository = Depends(get_client_repository),
) -> ClientService:
    return ClientService(repository)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/clients/login"
)

def get_current_client(
    token: str = Depends(oauth2_scheme)
):
    client = token.s
