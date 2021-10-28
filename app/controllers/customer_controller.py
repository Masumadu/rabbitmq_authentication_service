from app.core.result import Result
from app.core.service_result import ServiceResult
from app.repositories import CustomerRepository
from app.core.notifications.notifier import Notifier
from app.services import EmailNotification

notification_handler = Notifier()
email_notification = EmailNotification()


class CustomerController:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def index(self):
        customers = self.customer_repository.index()
        return ServiceResult(Result(customers, 200))

    def create(self, data):
        customer = self.customer_repository.create(data)
        email_notification.recipient = "michaelasumadu10@gmail.com"
        notification_handler.notify(email_notification)
        return ServiceResult(Result(customer, 201))

    def find_by_id(self, obj_id):
        customer = self.customer_repository.find_by_id(obj_id)
        return ServiceResult(Result(customer, 200))