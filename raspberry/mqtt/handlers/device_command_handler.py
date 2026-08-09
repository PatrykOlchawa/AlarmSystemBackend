from mqtt.schemas import MQTTMessage, DeviceCommandPayload
from gpio.device_manager import DeviceManager
from mqtt.publishers.device_state_publisher import DeviceStatePublisher
from pydantic import ValidationError
import logging
logger = logging.getLogger(__name__)
class DeviceCommandHandler:
    def __init__(
        self,
        device_manager: DeviceManager,
        device_state_publisher: DeviceStatePublisher,
    ):
        self.device_manager = device_manager
        self.device_state_publisher = device_state_publisher
        
    def handle(
        self,
        message: MQTTMessage,
    ):
        try:
            payload = DeviceCommandPayload.model_validate_json(
                message.payload 
            )

            if message.resource_id is None:
                logger.warning(
                    "Device command without device_id"
                )
                return

            device_id = message.resource_id
            self.device_manager.set_state(
                device_id= device_id,
                status=payload.root,
            )
            device = self.device_manager.get(device_id=device_id)
            print(
                    f"Device {device_id} found"
                )
            if device is None:
                print(
                    "Device %s not found",
                    device_id,
                )
                return

            self.device_state_publisher.publish(
                device_id = device_id,
                payload = device.status,
            )
        except ValidationError as exc:
            print(
                "Invalid command payload %s",
                exc,
            )

        except Exception:
            print(
                "Failed to process command"
            )