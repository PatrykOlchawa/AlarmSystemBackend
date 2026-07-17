from app.modules.notifications.repository import NotificationRepository
from app.core.exceptions import (
    NotificationNotFoundException,
)
from app.modules.notifications.model import Notification
from app.modules.notifications.schemas import NotificationCreate, NotificationUpdate

class NotificationService:
    def __init__(
        self,
        repository: NotificationRepository
    ):
        self.repository = repository
    
    def get_all(self):
        return self.repository.get_all()

    def get_by_id(
        self,
        notification_id: int
    ):
        notification = self.repository.get_by_id(notification_id)

        if notification is None:
            raise NotificationNotFoundException()
        
        return notification
    
    def get_by_user(
        self,
        user_id: int
    ):
        return self.repository.get_by_user_id(user_id)

    def get_unread_by_user(
        self,
        user_id: int
    ):
        return self.repository.get_unread_by_user(user_id)
    
    def get_latest_by_user(
        self,
        user_id: int
    ):
        return self.repository.get_latest_by_user(user_id)
    
    def get_unread_count(
        self,
        user_id: int
    ):
        return self.repository.get_unread_count(user_id)
    
    def create(
        self,
        request: NotificationCreate,
    ):
        notification = Notification(
            title=request.title,
            message=request.message,
            user_id=request.user_id,
            is_read=request.is_read,
            notification_type=request.notification_type,
        )
        return self.repository.create(notification)
    
    def update(
        self,
        notification_id: int,
        request: NotificationUpdate,
    ):
        notification = self.get_by_id(notification_id)
        notification.is_read = request.is_read
        
        return self.repository.update(notification)
    
    def delete(
        self,
        notification_id: int,
    ):
        notification = self.get_by_id(notification_id)
        
        self.repository.delete(notification)