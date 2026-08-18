import httpx
import logging

from app.modules.push_tokens.repository import PushTokenRepository

logger = logging.getLogger(__name__)

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"


class PushNotificationService:

    def __init__(
        self,
        push_token_repository: PushTokenRepository,
    ):
        self.push_token_repository = push_token_repository

    def send_to_user(
        self,
        user_id: int,
        title: str,
        message: str,
        data: dict | None = None,
    ) -> None:

        tokens = self.push_token_repository.get_by_user_id(
            user_id
        )

        if not tokens:
            return

        messages = [
            {
                "to": token.token,
                "title": title,
                "body": message,
                "data": data or {},
                "sound": "default",
            }
            for token in tokens
        ]

        try:
            response = httpx.post(
                EXPO_PUSH_URL,
                json=messages,
                timeout=10,
            )

            response.raise_for_status()

            logger.info(
                "Push notifications sent to user=%s",
                user_id,
            )

        except Exception:
            logger.exception(
                "Failed to send push notifications"
            )

    def _send(
        self,
        token: str,
        title: str,
        message: str,
        data: dict,
    ) -> None:

        payload = {
            "to": token,
            "title": title,
            "body": message,
            "data": data,
            "sound": "default",
        }

        try:
            response = httpx.post(
                EXPO_PUSH_URL,
                json=payload,
                timeout=10,
            )

            response.raise_for_status()

            logger.info(
                "Push notification sent to %s",
                token,
            )

        except Exception:
            logger.exception(
                "Failed to send push notification"
            )