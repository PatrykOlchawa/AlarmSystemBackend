from mediaMTX.mediamtx_client import MediaMTXClient
import logging
logger = logging.getLogger(__name__)
class CameraController:

    def __init__(
        self,
        mediamtx_client: MediaMTXClient,
    ):
        self.mediamtx_client = mediamtx_client

    def configure_camera_path(
        self,
        path: str,
        existing_paths: set[str],
    ) -> None:

        config = {
            "source": (f"rtsp://127.0.0.1:18554/{path}"),
            "rtspTransport": "tcp",
        }

        if path in existing_paths:
            logger.info(
                "MediaMTX path=%s already exists, updating",
                path,
            )

            self.mediamtx_client.patch_path(
                path=path,
                config=config,
            )

            return

        logger.info(
            "Creating MediaMTX path=%s",
            path,
        )

        self.mediamtx_client.create_path(
            path=path,
            config=config,
        )

    def delete_camera_path(
        self,
        path: str,
    ) -> None:

        self.mediamtx_client.delete_path(
            path=path,
        )

    def get_paths(self) -> list[str]:
        return self.mediamtx_client.get_paths()