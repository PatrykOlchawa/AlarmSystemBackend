import requests
from config import settings

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = settings.api_url
        self.access_token = None

    def set_access_token(
        self,
        token: str,
    ):
        self.access_token = token

        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}"
            }
        )

    def get(
        self,
        path: str,
    ):
        response = self.session.get(
            f"{self.base_url}{path}"
        )

        response.raise_for_status()

        return response.json()

    def post(
        self,
        path: str,
        data: dict,
    ):
    
        response = self.session.post(
            f"{self.base_url}{path}",
            json=data,
        )

        response.raise_for_status()

        return response.json()

api_client = APIClient()