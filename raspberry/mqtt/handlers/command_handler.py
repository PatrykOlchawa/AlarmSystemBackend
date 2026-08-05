from raspberry.mqtt.schemas import MQTTMessage, CommandPayload
class CommandHandler:
    def handle(
        self,
        message: MQTTMessage,
    ):
        payload = CommandPayload.model_validate_json(
            message.payload 
        )

        