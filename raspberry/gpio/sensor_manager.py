from common.schemas import (
    ConfigResponse,
    SensorConfig,
    SensorType,
)

class SensorManager:
    def __init__(self):
        self.sensors: dict[int, SensorConfig] = {}
        self.gpio_map: dict[int, SensorConfig] = {}

    def configure(
        self,
        config: ConfigResponse,
    ) -> None:
        self.sensors.clear()
        self.gpio_map.clear()


        for sensor in config.sensors:
            gpio = sensor.gpio_pin

            self.sensors[sensor.id] = sensor
            self.gpio_map[gpio] = sensor

            print(
                f"Configured {sensor.type.value} "
                f"{sensor.name} "
                f"GPIO={gpio}"
            )

    def get(
        self,
        sensor_id: int,
    ) -> SensorConfig:
        return self.sensors[sensor_id]
    
    def get_by_gpio(
        self,
        gpio: int,
    ) -> SensorConfig:
        return self.gpio_map[gpio]
    
    def get_all(
        self,
    ) -> list[SensorConfig]:
        return list(self.sensors.values())

    def exists(
        self,
        sensor_id: int,
    ) -> bool:
        return sensor_id in self.sensors

    def gpio_exists(
        self,
        gpio: int,
    ) -> bool:
        return gpio in self.gpio_map
    
    def configure_gpio(
        self,
    ) -> None:
        for sensor in self.sensors.values():
            print(
                f"GPIO {sensor.connection_identifier}"
                f"configured for {sensor.name}"
            )
            #GPIO.setup(pin, GPIO.out)

    def read(
        self,
        sensor_id: int,
    ) -> None:
        sensor = self.sensors[sensor_id]

        print(
            f"Reading {sensor.name}"
        )
        #if sensor.type == SensorType.PIR:
        #    return 0

        #if sensor.type == SensorType.LDR:
        #    return 500

        #if sensor.type == SensorType.TEMPERATURE:
        #    return 50
        return None