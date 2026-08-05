from sqlalchemy import(
    select,
    update
) 
from sqlalchemy.orm import(
    Session,
    selectinload,

)
from app.modules.clients.model import Client
from app.modules.alarms.model import Alarm

class ClientRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(
        self,
        alarm: Alarm,
    ) -> list[Client]:
        stmt = (
            select(Client)
            .where(Client.alarm_id == alarm.id)
        )
        return self.session.scalars(stmt).all()

    def get_by_client_id(
        self,
        client_id: str,
    ) -> Client | None:
        stmt = (
            select(Client)
            .where(Client.client_id == client_id)
        )
        return self.session.scalar(stmt)

    def create(
        self,
        client: Client,
    ) -> Client:
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)   
        return client

    def update(
        self,
        client: Client,
    ) -> Client:
        self.session.commit()
        self.session.refresh(client)
        return client

    def delete(
        self,
        client:Client,
    ) -> None:
        self.session.delete(client)
        self.session.commit()