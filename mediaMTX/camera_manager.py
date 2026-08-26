from camera_controller import CameraController
from app.common.enums import DeviceType
from mediaMTX.schemas import CamerasConfigPayload

import logging

logger = logging.getLogger(__name__)


class CameraManager:

    def __init__(
        self,
        camera_controller: CameraController,
    ):
        self.camera_controller = camera_controller

    def configure(
        self,
        alarm_id: int,
        config: CamerasConfigPayload,
    ) -> None:

        existing_paths = set(
            self.camera_controller.get_paths()
        )

        desired_paths: set[str] = set()

        for camera in config.cameras:

            path = camera.path

            desired_paths.add(path)

            self._configure_camera(
                path=path,
                existing_paths=existing_paths,
            )

        self._remove_old_paths(
            alarm_id=alarm_id,
            existing_paths=existing_paths,
            desired_paths=desired_paths,
        )

    def _configure_camera(
        self,
        path: str,
        existing_paths: set[str],
    ) -> None:
        logger.info(
            "Configuring camera path=%s",
            path,
        )
        self.camera_controller.configure_camera_path(
            path=path,
            existing_paths=existing_paths,
        )

    def _remove_old_paths(
        self,
        alarm_id: int,
        existing_paths: set[str],
        desired_paths: set[str],
    ) -> None:

        prefix = f"alarm-{alarm_id}-camera"

        for path in existing_paths:

            if not path.startswith(prefix):
                continue

            if path in desired_paths:
                continue

            logger.info(
                "Removing old MediaMTX path %s",
                path,
            )

            self.camera_controller.delete_camera_path(
                path=path,
            )