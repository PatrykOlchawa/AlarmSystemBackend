import logging
from storage.config_store import ConfigStore
from mqtt.client import MQTTClient
from mqtt.dispatcher import MQTTDispatcher
from gpio.device_manager import DeviceManager
from gpio.alarm_manager import AlarmManager
from gpio.sensor_manager import SensorManager
from mqtt.publishers.device_state_publisher import DeviceStatePublisher
from mqtt.publishers.alarm_state_publisher import AlarmStatePublisher
from mqtt.publishers.sensor_publisher import SensorPublisher
from mqtt.handlers.alarm_command_handler import AlarmCommandHandler
from mqtt.handlers.device_command_handler import DeviceCommandHandler
from api.auth_service import auth_service
from api.config_service import config_service
from storage.config_store import config_store
import threading

logger = logging.getLogger(__name__)

def main():

    print("Loggin in...")

    auth_service.login()

    print("Downloading configuration")

    config = config_service.get_config()

    config_store.save(config)

    print(config_store.load())
    # 2. Pobranie ID alarmu z konfiguracji
    alarm_id = config.alarm.id

    # 3. Utworzenie managerów
    device_manager = DeviceManager()
    sensor_manager = SensorManager()
    alarm_manager = AlarmManager()


    # 4. MQTT client
    mqtt_client = MQTTClient(alarm_id=alarm_id)

    # 5. Publishers
    alarm_state_publisher = AlarmStatePublisher(
        mqtt_client=mqtt_client,
    )

    device_state_publisher = DeviceStatePublisher(
        mqtt_client=mqtt_client,
    )

    sensor_publisher = SensorPublisher(
        mqtt_client=mqtt_client,
    )

    device_manager.configure(config)
    sensor_manager.configure(config)
    # 6. Handlers
    alarm_command_handler = AlarmCommandHandler(
        alarm_manager=alarm_manager,
        alarm_state_publisher=alarm_state_publisher,
    )

    device_command_handler = DeviceCommandHandler(
        device_manager=device_manager,
        device_state_publisher=device_state_publisher,
    )

    # 7. Dispatcher
    dispatcher = MQTTDispatcher(
        device_command_handler=device_command_handler,
        alarm_command_handler=alarm_command_handler,
    )

    # 8. Podłączenie dispatchera do MQTT
    mqtt_client.set_dispatcher(dispatcher)

    # 9. Uruchomienie MQTT
    mqtt_client.start()

    logger.info(
        "Raspberry alarm application started"
    )

    # 10. Utrzymanie procesu przy życiu
    stop_event = threading.Event()

    try:
        stop_event.wait()

    except KeyboardInterrupt:
        logger.info(
            "Stopping Raspberry alarm application"
        )

    finally:
        mqtt_client.stop()


if __name__ == "__main__":
    main()