# local import
from app import db
from config import Config
# builtin imports
from dataclasses import dataclass
import jwt

# third party imports
from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class CustomerModel(db.Model):
    """
    Table schema for recording customer info
    """
    id: int
    name: str
    username: str
    email: str
    password: str

    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.String, nullable=False)
    username = db.Column('username', db.String, nullable=False, unique=True)
    email = db.Column('Email', db.String, nullable=False, unique=True)
    hash_password = db.Column('Password', db.String, nullable=False)
    verification_status = db.Column("Account Verification", db.Boolean, nullable=False, default=False)

    @property
    def password(self):
        return self.hash_password

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password, method="sha256")

    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)

    @staticmethod
    def verify_account_verification_token(token):
        try:
            id = jwt.decode(token, Config.SECRET_KEY,
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return id

    def __repr__(self):
        return f"<Customer: {self.name}>"
