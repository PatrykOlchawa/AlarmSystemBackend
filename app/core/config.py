from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Alarm System API"
    debug: bool

    database_url: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    mqtt_host: str
    mqtt_port: int
    mqtt_username: str
    mqtt_password: str
    mqtt_client_id: str
    
    model_config = SettingsConfigDict(
        env_file=".env"
    )



settings = Settings()