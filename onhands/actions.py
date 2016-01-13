from functools import wraps


def action(url):
    def dec(func):
        func._action_url = url.replace('/', '')

        @wraps(func)
        def inner(*arg, **kw):
            return func(*arg, **kw)
        return inner
    return dec


class ActionAPI(object):

    @classmethod
    def get_action(cls, url, model_id):
        for clazz in cls.__subclasses__():
            for methodname in clazz.__dict__:
                method = getattr(clazz(), methodname)
                if hasattr(method, '_action_url') and url == method._action_url:
                    return method(model_id)
