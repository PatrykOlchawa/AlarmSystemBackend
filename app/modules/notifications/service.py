from app.modules.alarms.model import Alarm
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
    
    def get_all(
        self,
        alarm: Alarm,
    ):
        return self.repository.get_all(alarm)

    def get_by_id(
        self,
        alarm: Alarm,
        notification_id: int,
    ):
        notification = self.repository.get_by_id(alarm, notification_id)

        if notification is None:
            raise NotificationNotFoundException()
        
        return notification
    
    def get_by_user(
        self,
        alarm: Alarm,
        user_id: int
    ):
        return self.repository.get_by_user_id(alarm, user_id)

    def get_unread_by_user(
        self,
        alarm: Alarm,
        user_id: int
    ):
        return self.repository.get_unread_by_user(alarm, user_id)
    
    def get_latest_by_user(
        self,
        alarm: Alarm,
        user_id: int
    ):
        return self.repository.get_latest_by_user(alarm, user_id)
    
    def get_unread_count(
        self,
        alarm: Alarm,
        user_id: int
    ):
        return self.repository.get_unread_count(alarm, user_id)
    
    def create(
        self,
        alarm: Alarm,
        request: NotificationCreate,
    ):
        notification = Notification(**request.model_dump())
        return self.repository.create(notification)
    
    def update(
        self,
        alarm: Alarm,
        notification_id: int,
        request: NotificationUpdate,
    ):
        notification = self.get_by_id(notification_id)
        notification.is_read = request.is_read
        
        return self.repository.update(notification)
    
    def delete(
        self,
        alarm: Alarm,
        notification_id: int,
    ):
        notification = self.get_by_id(notification_id)
        
        self.repository.delete(notification)