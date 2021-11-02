from flask_testing import TestCase
from app import create_app, db
import fakeredis
from unittest.mock import patch
from .initial_test_data import setup_data, model_data
from .test_responses import SharedResponse


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app("config.TestingConfig")
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()
        self.customer = setup_data()
        self.customer_model = model_data()
        db.session.add(self.customer_model)
        db.session.commit()
        self.patcher = patch("app.services.redis_service.redis_conn",
                             fakeredis.FakeStrictRedis())
        self.addCleanup(self.patcher.stop)
        self.redis = self.patcher.start()
        self.shared_responses = SharedResponse()


    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()
        self.patcher.stop()
