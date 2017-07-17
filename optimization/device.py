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

    def calculate_compatibility(self, widget, metric):
        assert isinstance(widget, Widget)
        if metric is 'distance':
            return self.distance(widget.requirements)
        elif metric is 'dot':
            return self.affordances.dot(widget.requirements)

    def has_access(self, user):
        return user in self.users

    def give_access(self, user):
        assert isinstance(user, User)
        self.users.append(user)

    def distance(self, widget_requirements):
        max_distance = 10
        distance = 0
        if widget_requirements.visual_display != 0:
            distance += (self.affordances.visual_display - widget_requirements.visual_display) ** 2
        if widget_requirements.text_input != 0:
            distance += (self.affordances.text_input - widget_requirements.text_input) ** 2
        if widget_requirements.touch_pointing != 0:
            distance += (self.affordances.touch_pointing - widget_requirements.touch_pointing) ** 2
        if widget_requirements.mouse_pointing != 0:
            distance += (self.affordances.mouse_pointing - widget_requirements.mouse_pointing) ** 2

        return max_distance - int(distance ** 0.5)

    def __repr__(self):
        return '[Device "%s" capacity=%d affordances=%s users=%s]' % (self.name, self.capacity, self.affordances, ','.join([u.name for u in self.users]))
