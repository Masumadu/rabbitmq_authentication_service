from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from app.utils import GUID
from flask_mail import Mail
from celery import Celery

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
mail = Mail()
celery = Celery()
# print(ext_celery)
# jwt = JWTManager()
db.__setattr__("GUID", GUID)

