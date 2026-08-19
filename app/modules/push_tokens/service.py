from app.core.exceptions import (
    InvalidPushTokenException,
)
from app.modules.push_tokens.schemas import (
    PushTokenRequest,
)
from app.modules.push_tokens.model import PushToken
from app.modules.push_tokens.repository import PushTokenRepository

class PushTokenService:
    def __init__(
        self,
        repository: PushTokenRepository,
    ):
        self.repository = repository

    def get_by_id(
        self,
        push_token_id: int,
    ) -> PushToken | None:
        token = self.repository.get_by_id(push_token_id)
        if token is None:
            raise InvalidPushTokenException
        return token
    
    def get_by_user(
        self,
        user_id: int,
    ) -> list[PushToken]:
        token = self.repository.get_by_user_id(user_id)
        return token

    def get_token(
        self,
        token:str,
    ) -> PushToken | None:
        
        token = self.repository.get_by_token(token)
        return token

    def create(
        self,
        user_id: int,
        request: PushTokenRequest,
    ) -> PushToken:

        existing = self.repository.get_by_token(request.token)

        if existing:
            existing.user_id = user_id
            existing.platform = request.platform
            existing.locale = request.locale
            existing.device_id = request.device_id
            existing.is_active = True

            return self.repository.update(existing)
      
        push_token = PushToken(
            user_id=user_id,
            **request.model_dump(),
        )
        push_token = self.repository.create(push_token)
        return push_token

    def delete(
        self,
        push_token_id: int,
        user_id: int,
    ) -> None:
        push_token = self.get_by_id(push_token_id)
        if push_token.user_id != user_id:
            raise InvalidPushTokenException

        self.repository.delete(push_token)

