from app.notifications.base import NotificationStrategy


class SMSNotification(NotificationStrategy):
    """Strategy Pattern — SMS implementasiyası."""

    def send(self, recipient: str, subject: str, message: str) -> bool:
        # Twilio və ya digər SMS API
        print(f"[SMS] To: {recipient} | Message: {message}")
        return True