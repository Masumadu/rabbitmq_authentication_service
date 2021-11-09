from app.producer import PikaClient
from app.core.notifications import NotificationHandler
# from config import Config


class NotificationService(NotificationHandler):
    email_info: dict
    sms_info: dict

    def __init__(self, notification_channels: list):
        self.notification_channels = notification_channels
        self.pika_client = PikaClient(queue="notification")

    def send(self):
        if "sms" in self.notification_channels and "email" in self.notification_channels:
            self.pika_client.publish_message([self.email_info, self.sms_info])
        elif "sms" in self.notification_channels:
            self.pika_client.publish_message([self.sms_info])
        elif "email" in self.notification_channels:
            self.pika_client.publish_message([self.email_info])
