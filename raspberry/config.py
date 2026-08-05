from dataclasses import dataclass

@dataclass
class MQTTSettings:
    host: str = "localhost"
    port: int = 1883
    username: str = "raspberry"
    password: str = "egregius@"
    client_id: str = "alarm-raspberry"
    
settings = MQTTSettings()