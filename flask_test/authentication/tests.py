from faker import Factory
from flask_testing import TestCase
from flask_test import create_app
from flask_test.models import db


class TestAuthentication(TestCase):

    def create_app(self):
        return create_app('testing')

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client
        self.faker = Factory.create()

        with self.app.app_context():
            # create all tables
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def test_login_with_valid_credentials(self):
        """
        Should login providing valid credentials
        """

        # Create a user first
        username = self.faker.email()
        password = self.faker.password()
        response = self.client().post('/users', json={
            'username': username,
            'email': self.faker.email(),
            'password': password,
            'password_confirm': password
        })
        self.assertEqual(response.status_code, 201)

        # Try to login now
        response = self.client().post('/login', json={
            'username': username,
            'password': password
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_login_with_invalid_credentials(self):
        """
        Should not login providing invalid credentials
        """

        response = self.client().post('/login', json={
            'username': self.faker.email(),
            'password': self.faker.password()
        })
        self.assertEqual(response.status_code, 401)
