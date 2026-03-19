from app.notifications.base import NotificationStrategy


class EmailNotification(NotificationStrategy):
    """
    Strategy Pattern — Email implementasiyası.
    """

    def send(self, recipient: str, subject: str, message: str) -> bool:
        # smtplib və ya fastapi-mail gelecekde
        print(f"[EMAIL] To: {recipient} | Subject: {subject} | Message: {message}")
        return True