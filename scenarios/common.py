# flake8: noqa
from user import User
from device import Device
from widget import Widget
from element import Element
from properties import Properties
import optimize_device_assignment

class Scenario(object):

    def __init__(self):
        from collections import OrderedDict
        self.elements = OrderedDict()
        self.devices = OrderedDict()
        self.users = OrderedDict()
        self.expectations = OrderedDict()

    def add_element(self, element):
        assert isinstance(element, Element)
        self.elements[element.name] = element

    def add_elements_from_text(self, text):
        lines = text.split('\n')
        lines = [line for line in lines if line.strip() > '']
        entries = [[entry.strip() for entry in line.split('|')] for line in lines]
        current_element = None
        for line_entries in entries:
            if line_entries[0] > '' and line_entries[1] > '':
                name = line_entries[0]
                importance = int(line_entries[1])
                current_element = Element(name, importance, widgets=[])
                self.add_element(current_element)

            # Create Widget from remaining values
            size = int(line_entries[2])
            visual_quality = int(line_entries[3])
            requirements = get_properties_from_code(line_entries[4])
            widget = Widget(size, requirements, visual_quality)
            current_element.widgets.append(widget)

    def add_devices_from_text(self, text):
        lines = text.split('\n')
        lines = [line for line in lines if line.strip() > '']
        entries = [[entry.strip() for entry in line.split('|')] for line in lines]
        for line_entries in entries:
            name = line_entries[0]
            capacity = int(line_entries[1])
            affordances = get_properties_from_code(line_entries[2])

            # Parse users
            users = []
            if line_entries[3] > '':
                users = [self.users[user_name.strip()]
                         for user_name in line_entries[3].split(',')]

            self.add_device(Device(name, capacity, affordances, users))

    def add_device(self, device):
        assert isinstance(device, Device)
        self.devices[device.name] = device

    def add_users(self, *names):
        for name in names:
            assert type(name) is str
            self.users[name] = User(name)

    def adjust_user_importance(self, user_name, element_name, value):
        user = self.users[user_name]
        user.importance[element_name] = value

    def expect(self, device_to_elements):
        self.expectations = device_to_elements

    def run(self):
        elements, devices, users = self.elements.values(), self.devices.values(), self.users.values()
        output = optimize_device_assignment.optimize(elements, devices, users)

        print('\nInputs')
        print('=======\n')
        print('Users: ' + ', '.join([u.name for u in users]))
        print('')
        for element in elements:
            print(element)
            print('No. of widgets: %d\n' % len(element.widgets))

        for device in devices:
            print(device)
            print('Users with access (%d): %s\n' % (len(device.users), ', '.join([user.name for user in device.users])))

        print('\nOutputs')
        print('=======\n')

        for device, values in output.items():
            print('%s <%d widget(s) assigned>' % (device.name, len(values)))
            for value in values:
                element = value['element']
                widget = value['widget']
                print('> %s: %s' % (element.name, widget))
            print('')

        # See if expectations fulfilled if specified previously
        if len(self.expectations) > 0:
            failure_msgs = []
            for device_name, element_names in self.expectations.iteritems():
                device = self.devices[device_name]
                for element_name in element_names:
                    element = self.elements[element_name]
                    if element not in [v['element'] for v in output[device]]:
                        failure_msgs += ['[FAIL] %s not assigned to %s' % (element_name, device_name)]

            print('\nTESTS')
            print('=====\n')
            if len(failure_msgs) == 0:
                print('Great! All expectations met.')
            else:
                print('%d FAILURE(S)' % len(failure_msgs))
                for i, msg in enumerate(failure_msgs):
                    print('(%d) %s' % (i + 1, msg))
                print('')
                raise Exception('Expectation(s) not met. Please check above.')


def get_properties_from_code(code):
    nums = [int(c) for c in code.strip()]
    return Properties(*nums)
