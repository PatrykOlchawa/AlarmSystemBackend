from pydantic import BaseModel

class CameraConfig(BaseModel):
    device_id: int
    path: str

class CamerasConfigPayload(BaseModel):
    cameras: list[CameraConfig]
