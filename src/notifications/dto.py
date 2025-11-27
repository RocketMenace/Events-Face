from dataclasses import dataclass, field


@dataclass(kw_only=True, frozen=True, eq=False)
class NotificationDTO:
    topic: str
    payload: dict = field(
        default_factory=dict,
        metadata={
            "confirmation_code": "Notification about successful registration on event",
        },
    )
