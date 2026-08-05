from fastapi import Depends
from sqlalchemy.orm import Session

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