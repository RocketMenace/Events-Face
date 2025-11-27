from .dto import NotificationDTO
from .models import NotificationModel


class NotificationsRepository:
    model = NotificationModel

    def create(self, dto: NotificationDTO) -> None:
        try:
            obj = self.model(
                topic=dto.topic,
                payload=dto.payload,
            )
            obj.full_clean()
            obj.save()
        except Exception:
            raise
