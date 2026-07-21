from app.modules.alarms.model import Alarm
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.modules.notifications.model import Notification

class NotificationRepository:
    def __init__(self, db_session: Session):
        self.session = db_session
    
    def get_all(
        self,
        alarm: Alarm
    ) -> list[Notification]:
        stmt = (select(Notification)
            .where(Notification.alarm_id == alarm.id)
            .order_by(Notification.timestamp.desc()))
        
        return list(self.session.scalars(stmt).all())
    
    def get_by_id(
        self,
        alarm: Alarm,
        notification_id: int,
    ) -> Notification | None:
        stmt = (select(Notification)
            .where(Notification.id == notification_id)
            .where(Notification.alarm_id == alarm.id)
        )
        return self.session.scalar(stmt)
    
    def get_by_user_id(
        self,
        alarm: Alarm,
        user_id: int,
    ) -> list[Notification]:
        stmt = (select(Notification)
            .where(Notification.alarm_id == alarm.id)
            .where(Notification.user_id == user_id)
        )
        return list(self.session.scalars(stmt).all())
    
    def get_unread_by_user(
        self,
        alarm: Alarm,
        user_id: int,
    ) -> list[Notification]:
        stmt = (select(Notification)
            .where(Notification.alarm_id == alarm.id)
            .where(
                Notification.user_id == user_id,
                Notification.is_read == False,
            )
            .order_by(Notification.timestamp.desc())

        )
        return list(self.session.scalars(stmt).all())
    def get_latest_by_user(
        self,
        alarm: Alarm,
        user_id: int,
    ) -> Notification | None:
        stmt = (select(Notification)
            .where(Notification.alarm_id == alarm.id)
            .where(Notification.user_id == user_id)
            .order_by(Notification.timestamp.desc())
            .limit(1)
        )
        return self.session.scalar(stmt)

    def get_unread_count(
        self,
        alarm: Alarm,
        user_id: int,
    ) -> int:
        stmt = (
            select(func.count())
            .select_from(Notification)
            .where(Notification.alarm_id == alarm.id)
            .where(
                Notification.user_id == user_id,
                Notification.is_read == False,
            )
        )
        return self.session.scalar(stmt) or 0

    def create(
        self,
        notification: Notification,
    ) -> Notification:
        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)
        return notification
    
    def update(
        self,
        notification: Notification,
    ) -> Notification:   

        self.session.commit()
        self.session.refresh(notification)

        return notification
    
    def delete(
        self,
        notification: Notification,
    ) -> None:
        self.session.delete(notification)
        self.session.commit()
    