from app.core.notifications import NotificationHandler
# from app.core.exceptions import AppException
from app.utils.task.task_scheduler import sum


class EmailNotification(NotificationHandler):
    recipient: str

    def send(self):
        sum.delay(5, 6)
        # from app.utils.task.task_scheduler import send_email
        # try:
        #     send_email.delay()
        # except send_email.OperationalError as exc:
        #     raise AppException.OperationError(context=exc.args[0])