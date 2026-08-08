from api.api_client import api_client
from common.schemas import ConfigResponse
class ConfigService:
    def get_config(
        self
    ) -> ConfigResponse:
        response = api_client.get(
            "/clients/config",
        )
        return ConfigResponse.model_validate(response)

config_service = ConfigService()