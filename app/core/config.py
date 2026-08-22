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

    #mediaMTX
    mediamtx_private_key_path: str
    mediamtx_token_expire_minutes: int = 10
    mediamtx_token_issuer: str = "https://api.wsb-alarm.pl"
    mediamtx_token_audience: str = "mediamtx"  
    mediamtx_key_id: str = "alarm-mediamtx-1"  
    model_config = SettingsConfigDict(
        env_file=".env"
    )



settings = Settings()