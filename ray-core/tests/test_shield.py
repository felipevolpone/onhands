
from webtest import TestApp as FakeApp

from ray.endpoint import endpoint
from ray.wsgi.wsgi import application
from ray.authentication import Authentication, register
from ray.shield import Shield

from tests.model_interface import ModelInterface
from .common import Test


class TestShield(Test):

    def test_shields(self):

        @register
        class MyAuth(Authentication):

            expiration_time = 5
            salt_key = 'ray_salt_key'

            @classmethod
            def authenticate(cls, login_data):
                if login_data['username'] == 'felipe' and login_data['password'] == '123':
                    return {'username': 'felipe'}

        @endpoint('/person', authentication=MyAuth)
        class PersonModel(ModelInterface):

            def __init__(self, *a, **k):
                self.login = None
                super(PersonModel, self).__init__(*a, **k)

            @classmethod
            def columns(cls):
                return ['id']

        class PersonShield(Shield):
            __model__ = PersonModel

            def get(self, info):
                return info['username'] == 'felipe'

        response = self.app.post_json('/api/_login', {"username": "felipe", "password": '123'})
        self.assertEqual(200, response.status_int)

        response = self.app.get('/api/person/')
        self.assertEqual(200, response.status_int)

        self.app = FakeApp(application)
        response = self.app.get('/api/person', expect_errors=True)
        self.assertEquals(401, response.status_int)

        self.app = FakeApp(application)
        response = self.app.post('/api/person/', expect_errors=True)
        self.assertIsNot(401, response.status_int)

        self.app = FakeApp(application)
        response = self.app.put('/api/person/', expect_errors=True)
        self.assertIsNot(404, response.status_int)

        self.app = FakeApp(application)
        response = self.app.delete('/api/person/', expect_errors=True)
        self.assertIsNot(404, response.status_int)
