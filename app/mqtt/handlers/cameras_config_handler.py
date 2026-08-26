from app.mqtt.schemas import (
    MQTTMessage,
    AlarmStatePayload,
)
from pydantic import ValidationError
from mediaMTX.camera_manager import CameraManager
from mediaMTX.schemas import CamerasConfigPayload
import logging
logger = logging.getLogger(__name__)
class CamerasConfigHandler:
    def __init__(
        self,
        camera_manager: CameraManager
    ):
        self.camera_manager = camera_manager

    def handle(
        self,
        message: MQTTMessage
    ):
        try:
            payload = CamerasConfigPayload.model_validate_json(
                message.payload
            )
            self.camera_manager.configure(
                alarm_id=message.alarm_id,
                config=payload,
            )

        except ValidationError as exc:

            logger.warning(
                "Invalid cameras config payload: %s",
                exc,
            )

        except Exception:

            logger.exception(
                "Unexpected error while processing "
                "cameras config message"
            )
