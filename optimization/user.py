import uuid

class User(object):
    name = ''
    id = None

    def __init__(self, name=''):
        self.name = name
        self.id = uuid.uuid4()  # random UUID

    def __repr__(self):
        return '[User %s]' % self.name
