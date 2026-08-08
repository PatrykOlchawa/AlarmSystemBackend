from pathlib import Path
import json
from common.schemas import (
    ConfigResponse,
)
class ConfigStore:
    def __init__(
        self,
        path: str = "config.json",
    ):
        self.path = Path(path)

    def save(
        self,
        config: ConfigResponse,
    ) -> None:
        with self.path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                config.model_dump(mode="json"),
                file,
                indent=4,
            )

    def load(
        self,
    ) -> ConfigResponse | None:
        if not self.path.exists():
            return None
        with self.path.open(
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        return ConfigResponse.model_validate(data)

    def exists(
        self,
    ) -> bool:
        return self.path.exists()

    def delete(
        self,
    ) -> None:
        if self.path.exists():
            self.path.unlink()

    def update(
        self,
        config: ConfigResponse,
    ) -> None:
        self.save(config)

config_store = ConfigStore()