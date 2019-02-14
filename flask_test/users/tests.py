from faker import Factory
from flask_testing import TestCase
from flask_test import create_app
from flask_test.models import db


class TestUsers(TestCase):

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

    def test_user_creation_with_valid_data(self):
        """
        Should create user with valid data provided
        """

        username = self.faker.email()
        password = self.faker.password()
        response = self.client().post('/users', json={
            'username': username,
            'email': self.faker.email(),
            'password': password,
            'password_confirm': password
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get('username', None), username)

    def test_user_creation_with_invalid_data(self):
        """
        Should not be able to create users with invalid data
        """

        username = self.faker.email()
        password = self.faker.password()
        response = self.client().post('/users', json={
            'username': username,
            'email': self.faker.email(),
            'password': password,
            'password_confirm': password + '_'
        })
        self.assertEqual(response.status_code, 400)
