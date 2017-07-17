import uuid

class User(object):
    name = ''
    id = None
    importance = {}

    def __init__(self, name='', id=None, importance={}):
        self.name = name
        self.id = id or str(uuid.uuid4())  # random UUID
        self.importance = importance

    def __repr__(self):
        return '[User %s uid=%s importance=%s]' % (self.name, self.id, self.importance)
