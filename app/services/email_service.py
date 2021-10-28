from app.core.notifications import NotificationHandler
from app.core.exceptions import AppException


class EmailNotification(NotificationHandler):
    recipient: str

    def send(self):
        from app.utils.task.task_scheduler import send_email
        try:
            send_email.delay()
        except send_email.OperationalError as exc:
            raise AppException.OperationError(context=exc.args[0])