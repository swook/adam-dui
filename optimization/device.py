from properties import Properties
from user import User
from widget import Widget

class Device:

    name = ''
    capacity = 0
    affordances = {}
    users = []

    def __init__(self, name, capacity, affordances, users=[]):
        assert isinstance(capacity, int) and capacity > 0
        assert affordances is not None and isinstance(affordances, Properties)

        self.name = name
        self.capacity = capacity
        self.affordances = affordances
        self.users = users

    def calculate_compatibility(self, widget):
        assert isinstance(widget, Widget)

        compatibility = 0
        for key, value in self.affordances.items():
            if key not in widget.requirements:
                raise LookupError('No such property: %s' % key)
            compatibility += widget.requirements[key] * value
        return compatibility

    def has_access(self, user):
        return user in self.users

    def give_access(self, user):
        assert isinstance(user, User)
        self.users.append(user)

    def __repr__(self):
        return '[Device %s (%d)]' % (self.name, self.capacity)
