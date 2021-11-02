from marshmallow import Schema, fields


class CustomerSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)

    class Meta:
        ordered = True


class CreateCustomerSchema(CustomerSchema):
    class Meta:
        fields = ["id", "name", "username", "email", "password"]
        load_only = ["password"]


class ReadCustomerSchema(CustomerSchema):
    class Meta:
        fields = ["id", "name", "username", "email", "password"]
        load_only = ["password"]
