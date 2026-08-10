from dataclasses import dataclass


@dataclass
class Settings:
    api_url: str = "https://api.wsb-alarm.pl"

#    client_id: str = "3c5cd667-4dbd-404e-978d-3108a12f80cc"
 #   secret: str = "_wKma7nyMJ-MXoFKx-9tXOZ9T7X0zFHJ5FCxVfAx7D0"
    client_id = "e31bc6d5-5a76-4542-ab0f-2081abe420e9"
    secret = "F5u9iOCuQaInqbjuFRZESZWuH0dfFol3URkRaGMp4bU"

settings = Settings()