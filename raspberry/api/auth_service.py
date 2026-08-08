from api.api_client import api_client
from config import settings

class ClientAuthService:
    def login(self):
        response = api_client.post(
            "/clients/login",
            {
                "client_id": settings.client_id,
                "secret": settings.secret,
            }
        )

        api_client.set_access_token(
            response["access_token"]
        )

        return response

auth_service = ClientAuthService()