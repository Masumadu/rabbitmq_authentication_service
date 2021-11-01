from app.core.notifications import NotificationHandler
from app.producer import create_email_queue, create_sms_queue


class NotificationService(NotificationHandler):
    email_info: dict
    sms_info: dict

    def __init__(self, notification_channels: list):
        self.notification_channels = notification_channels

    def send(self):
        if "sms" in self.notification_channels and "email" in self.notification_channels:
            create_email_queue(self.email_info)
            create_sms_queue(self.sms_info)
        elif "sms" in self.notification_channels:
            create_sms_queue(self.sms_info)
        elif "email" in self.notification_channels:
            create_email_queue(self.email_info)
