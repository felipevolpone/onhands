
class Hook(object):

    methods = ['before_save', 'before_delete', 'after_save']

    def before_save(self, entity):
        """
            before_save it's the final moment before the entity being save.
            if the methods return true, the entity will be saved, if doesnt
            will not.
        """
        raise NotImplementedError

    def before_delete(self, entity):
        raise NotImplementedError()
        # FIXME its not raising exception on the same way that before_save is

    def after_save(self, entity):
        """
            after_save it's the moment after the entity is saved.
        """
        raise NotImplementedError
