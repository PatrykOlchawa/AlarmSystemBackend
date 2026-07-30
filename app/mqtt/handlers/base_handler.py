from abc import ABC, abstractmethod

from app.mqtt.schemas import MQTTMessage


class BaseHandler(ABC):

    @abstractmethod
    def handle(
        self,
        message: MQTTMessage,
    ) -> None:
        pass