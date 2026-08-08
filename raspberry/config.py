from dataclasses import dataclass


@dataclass
class Settings:
    api_url: str = "http://localhost:8000"

    client_id: str = "3c5cd667-4dbd-404e-978d-3108a12f80cc"
    secret: str = "_wKma7nyMJ-MXoFKx-9tXOZ9T7X0zFHJ5FCxVfAx7D0"


settings = Settings()