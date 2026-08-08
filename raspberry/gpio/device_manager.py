from raspberry.common.schemas import (
    ConfigResponse,
    DeviceConfig,
)

class DeviceManager:
    def __init__(self):
        self.devices: dict[int, DeviceConfig] = {}
        self.gpio_map: dict[int, DeviceConfig] = {}


    def configure(
        self,
        config: ConfigResponse,
    ) -> None:
        self.devices.clear()
        self.gpio_map.clear()


        for device in config.devices:
            gpio = int(device.connection_identifier)

            self.devices[device.id] = device
            self.gpio_map[gpio] = device
            print(
                f"Configured {device.type.value} "
                f"{device.name} "
                f"GPIO={gpio}"
            )

    def get(
        self,
        device_id: int,
    ) -> DeviceConfig:
        return self.devices[device_id]

    def get_by_gpio(
        self,
        gpio: int,
    ) -> DeviceConfig:
        return self.gpio_map[gpio]
    
    def get_all(
        self,
    ) -> list[DeviceConfig]:
        return list(self.devices.values())

    def exists(
        self,
        device_id: int,
    ) -> bool:
        return device_id in self.devices

    def gpio_exists(
        self,
        gpio: int,
    ) -> bool:
        return gpio in self.gpio_map
    
    def configure_gpio(
        self,
    ) -> None:
        for device in self.devices.values():
            print(
                f"GPIO {device.connection_identifier}"
                f"configured for {device.name}"
            )
            #GPIO.setup(pin, GPIO.out)

    def set_state(
        self,
        device_id: int,
        status: dict,
    ) -> None:
        device = self.devices[device_id]

        print(
            f"Set {device.name} -> {status}"
        )
        #match device.type