import json
from app.core.result import Result
from app.core.service_result import ServiceResult
from app.repositories import CustomerRepository
from app.core.notifications.notifier import Notifier
from app.services import NotificationService
from app.models import CustomerModel
from app.schema import ReadCustomerSchema
from flask import url_for, jsonify
from app.services import AuthService


customer_serializer = ReadCustomerSchema()
auth_service = AuthService()
notification_handler = Notifier()
notification_service = NotificationService(["email", "sms"])


class CustomerController:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def index(self):
        customers = self.customer_repository.index()
        return ServiceResult(Result(customers, 200))

    def create(self, data):
        customer = self.customer_repository.create(data)
        if customer:
            customer_info = json.loads(customer_serializer.dumps(customer))
            token = customer.get_customer_token()
            customer_info["url"] = url_for("customer.account_verification",
                                           token=token, _external=True)
            notification_service.email_info = customer_info
            notification_service.sms_info = {"phone": "024040404"}
            notification_handler.notify(notification_service)
        return ServiceResult(Result(customer, 201))

    def verify_account(self, token):
        account_id = CustomerModel.verify_account_verification_token(token)
        if account_id:
            self.update({"id": account_id}, {"verification_status": True})
            return jsonify("account verification successful")
        return jsonify("account verification unsuccessful")

    def update(self, query_info, obj_in):
        customer = self.customer_repository.update(query_info, obj_in)
        return ServiceResult(Result(customer, 200))

    def sign_in(self, obj_in):
        return auth_service.sign_in(auth_info=obj_in, model=CustomerModel)
