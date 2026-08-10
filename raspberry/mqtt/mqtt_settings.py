from dataclasses import dataclass

@dataclass
class MQTTSettings:
    #host: str = "localhost"
    host: str = "130.61.48.202"
    port: int = 1883
    username: str = "raspberry"
    password: str = "egregius@"
    client_id: str = "alarm-raspberry"
    
mqtt_settings = MQTTSettings()

