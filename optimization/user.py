import uuid

class User(object):
    name = ''
    id = None
    importance = None

    def __init__(self, name='', id=None, importance=None):
        self.name = name
        self.id = id or str(uuid.uuid4())  # random UUID
        self.importance = importance or {}

    def __repr__(self):
        return '[User %s uid=%s importance=%s]' % (self.name, self.id, self.importance)
