from app.notifications.base import NotificationStrategy


class AppNotification(NotificationStrategy):
    """Strategy Pattern — App push notification implementasiyası."""

    def send(self, recipient: str, subject: str, message: str) -> bool:
        # Firebase FCM gelecekde
        print(f"[APP] To: {recipient} | Subject: {subject} | Message: {message}")
        return True