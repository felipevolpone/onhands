import unittest
from onhands.api.api import app, OnHandsSettings
from onhands.api.endpoint import endpoint
import webapp2
from alabama.models import StringProperty, IntegerProperty, BaseModel
from alabama import connection

database = connection.start_db('db.properties')
connection.create_pool(database)


@endpoint('/user')
class UserModel(BaseModel):
    name = StringProperty()
    age = IntegerProperty()


class TestRouter(unittest.TestCase):

    @unittest.skip('skip')
    def test_basic_router(self):
        request = webapp2.Request.blank('/api/')
        response = request.get_response(app)
        self.assertEqual(200, response.status_int)

    def test_url_via_package(self):
        OnHandsSettings.ENDPOINT_MODULES = 'tests.test_router'

        request = webapp2.Request.blank('/api/user')
        request.json = {"name": "felipe"}
        request.method = 'GET'

        response = request.get_response(app)
        print response.json
        # self.assertEqual(response.to_json(), {'age': None, 'name': 'felipe', 'key': 1})
        self.assertEqual(201, response.status_int)
