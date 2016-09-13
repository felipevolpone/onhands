import unittest
from ray.hooks import Hook
from ray.model import Model


class UserHookUseless(Hook):
    pass


class UserWithUselessHook(Model):
    hooks = [UserHookUseless]


class UserHookException(Hook):
    def before_save(self, user):
        raise Exception('Any exception %s' % (user.name,))


class UserHookFalse(Hook):
    def before_save(self, user):
        return False


class UserHookTrue(Hook):
    def before_save(self, user):
        return True


class User(Model):
    hooks = [UserHookException]

    def __init__(self, name=None):
        self.name = name


class UserWithTwoHooks(Model):
    hooks = [UserHookTrue, UserHookFalse]


class TestHookBeforeSave(unittest.TestCase):

    def test_before_save_hook_case_exception(self):
        user = User(name='felipe')
        with self.assertRaises(Exception) as e:
            user.put()
        self.assertEqual(str(e.exception), 'Any exception felipe')

    def test_before_save_hook_with_two_hooks(self):
        user = UserWithTwoHooks()
        with self.assertRaises(Exception) as e:
            user.put()
        self.assertEqual(str(e.exception), 'The hook(s) UserHookFalse.before_save didnt return True')

    def test_hook_before_save_not_implemented(self):
        user = UserWithUselessHook()
        with self.assertRaises(NotImplementedError) as e:
            user.put()


class UserDeleteHookTrue(Hook):
    def before_delete(self, user):
        return bool(user.name)


class UserDelete(Model):
    hooks = [UserDeleteHookTrue]

    def __init__(self, name=None):
        self.name = name


class TestHookBeforeDelete(unittest.TestCase):

    def test_before_delete_exception(self):
        u = UserDelete()
        with self.assertRaises(Exception) as e:
            u.delete()
        self.assertEqual(str(e.exception), 'The hook UserDeleteHookTrue.before_delete didnt return True')

    def test_before_delete(self):
        u = UserDelete(name="ray")
        self.assertTrue(u.delete())

    def test_before_delete_not_implemented(self):
        class UserDeleteHookTrue(Hook):
            pass

        class UserDelete(Model):
            hooks = [UserDeleteHookTrue]

        u = UserDelete()
        self.assertTrue(u.delete())
