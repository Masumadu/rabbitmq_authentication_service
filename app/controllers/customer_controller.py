from app.core.result import Result
from app.core.service_result import ServiceResult
from app.repositories import CustomerRepository
from app.core.notifications.notifier import Notifier
from app.services import NotificationService
from app.models import CustomerModel
from app.services import AuthService
from app.utils.message_queue_body import sms_queue_body, mail_queue_body


auth_service = AuthService()
notification_handler = Notifier()
notification_service = NotificationService(["email"])


class CustomerController:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def index(self):
        customers = self.customer_repository.index()
        return ServiceResult(Result(customers, 200))

    def create(self, data):
        customer = self.customer_repository.create(data)
        if customer:
            notification_service.email_info = mail_queue_body(customer)
            # notification_service.sms_info = sms_queue_body(customer)
            notification_handler.notify(notification_service)
        return ServiceResult(Result(customer, 201))

    def verify_account(self, token):
        account_id = CustomerModel.verify_account_verification_token(token)
        if account_id:
            self.update({"id": account_id}, {"verification_status": True})
            return {
                "status": "success",
                "msg": "account verification successful"
            }
        return {
            "status": "error",
            "msg": "account verification unsuccessful"
        }

    def update(self, query_info, obj_in):
        customer = self.customer_repository.update(query_info, obj_in)
        return ServiceResult(Result(customer, 200))

    def sign_in(self, obj_in):
        return auth_service.sign_in(auth_info=obj_in, model=CustomerModel)
