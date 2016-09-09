from ray.actions import ActionAPI, action
from ray.endpoint import endpoint
from ray.application import ray_conf

from tests.model_interface import ModelInterface

import unittest


@endpoint('/user')
class UserModel(ModelInterface):

    def __init__(self, *a, **k):
        self.name = None
        self.age = None
        super(UserModel, self).__init__(*a, **k)

    def describe(self):
        return {'name': str, 'age': int}


class UserAction(ActionAPI):
    __model__ = UserModel

    @action('activate')
    def activate(self, parameters):
        pass


class TestActionMapping(unittest.TestCase):

    def test(self):
        self.assertTrue('user/activate' in ray_conf['action'])
