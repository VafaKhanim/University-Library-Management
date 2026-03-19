from app.notifications.base import NotificationStrategy


class EmailNotification(NotificationStrategy):
    """
    Strategy Pattern — Email implementasiyası.
    Real layihədə burda SMTP və ya SendGrid olardı.
    """

    def send(self, recipient: str, subject: str, message: str) -> bool:
        # smtplib və ya fastapi-mail
        print(f"[EMAIL] To: {recipient} | Subject: {subject} | Message: {message}")
        return True