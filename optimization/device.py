from properties import Properties
from element import Element
from user import User

class Device:

    name = ''
    width = 0
    height = 0
    affordances = {}
    users = []

    def __init__(self, name, width, height, affordances, users=[]):
        assert isinstance(width, int) and width > 0
        assert isinstance(height, int) and height > 0
        assert affordances is not None and isinstance(affordances, Properties)

        self.name = name
        self.affordances = affordances
        self.users = users

        self.width = width
        self.height = height
        self._area = width * height

    def calculate_compatibility(self, element, metric):
        assert isinstance(element, Element)
        if metric is 'distance':
            return self.distance(element.requirements)
        elif metric is 'dot':
            return self.affordances.dot(element.requirements)

    def has_access(self, user):
        return user in self.users

    def give_access(self, user):
        assert isinstance(user, User)
        if user not in self.users:
            self.users.append(user)

    def distance(self, element_requirements):
        max_distance = 10
        distance = 0
        if element_requirements.visual_display != 0:
            distance += (self.affordances.visual_display - element_requirements.visual_display) ** 2
        if element_requirements.text_input != 0:
            distance += (self.affordances.text_input - element_requirements.text_input) ** 2
        if element_requirements.touch_pointing != 0:
            distance += (self.affordances.touch_pointing - element_requirements.touch_pointing) ** 2
        if element_requirements.mouse_pointing != 0:
            distance += (self.affordances.mouse_pointing - element_requirements.mouse_pointing) ** 2

        return max_distance - int(distance ** 0.5)

    def __repr__(self):
        return '[Device "%s" size=(%d,%d) affordances=%s users=%s]' % \
                (self.name, self.width, self.height, self.affordances,
                 ','.join([u.name for u in self.users]))
