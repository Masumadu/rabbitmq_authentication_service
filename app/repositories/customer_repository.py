# local imports
from app.core.repository import SQLBaseRepository
from app.models import CustomerModel
from app.services import RedisService
from app.schema import CustomerSchema
from app.core.exceptions import HTTPException

customer_schema = CustomerSchema()


class CustomerRepository(SQLBaseRepository):
    model = CustomerModel

    def __init__(self, redis_service: RedisService):
        self.redis_service = redis_service
        super().__init__()

    def index(self):
        try:
            redis_all_customers = self.redis_service.get("all_customers")
            if redis_all_customers:
                return redis_all_customers
            return super().index()
        except HTTPException:
            return super().index()

    def create(self, obj_in):
        postgres_create_customer = super().create(obj_in)
        serialize_all_customers_info = customer_schema.dumps(super().index(),
                                                             many=True)
        serialize_customer_info = customer_schema.dumps(
            postgres_create_customer)
        try:
            self.redis_service.set(f"customer__{postgres_create_customer.id}",
                                   serialize_customer_info)
            self.redis_service.set("all_customers",
                                   serialize_all_customers_info)
        except HTTPException:
            return postgres_create_customer
        else:
            return postgres_create_customer

    def find_by_id(self, obj_id: int):
        try:
            cached_data = self.redis_service.get(f"customer__{obj_id}")
        except HTTPException:
            return super().find_by_id(obj_id)
        else:
            return cached_data
