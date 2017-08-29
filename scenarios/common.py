# flake8: noqa
import sys
sys.path.insert(0, '../optimization/')

from user import User
from device import Device
from element import Element
from properties import Properties
import optimize_device_assignment

class Scenario(object):

    def __init__(self):
        from collections import OrderedDict
        self.elements = OrderedDict()
        self.devices = OrderedDict()
        self.users = OrderedDict()

    def add_element(self, element):
        assert isinstance(element, Element)
        self.elements[element.name] = element

    def add_elements_from_text(self, text):
        lines = text.split('\n')
        lines = [line for line in lines if line.strip() > '']
        entries = [[entry.strip() for entry in line.split('|')] for line in lines]
        current_element = None
        for line_entries in entries:
            name = line_entries[0]
            importance, min_w, min_h, max_w, max_h = [int(v) for v in line_entries[1:6]]
            requirements = get_properties_from_code(line_entries[6])
            current_element = Element(name, importance, min_w, max_w, min_h, max_h, requirements)
            self.add_element(current_element)

    def add_devices_from_text(self, text):
        lines = text.split('\n')
        lines = [line for line in lines if line.strip() > '']
        entries = [[entry.strip() for entry in line.split('|')] for line in lines]
        for line_entries in entries:
            name = line_entries[0]
            width, height = [int(v) for v in line_entries[1:3]]
            affordances = get_properties_from_code(line_entries[3])

            # Parse users
            users = []
            if line_entries[4] > '':
                users = [self.users[user_name.strip()]
                         for user_name in line_entries[4].split(',')]

            self.add_device(Device(name, width, height, affordances, users))

    def add_device(self, device):
        assert isinstance(device, Device)
        self.devices[device.name] = device

    def remove_device_by_name(self, device_name):
        assert device_name in self.devices.keys()
        del self.devices[device_name]

    def add_users_by_names(self, *names):
        for name in names:
            assert type(name) is str
            self.users[name] = User(name)

    def remove_user_by_name(self, user_name):
        assert user_name in self.users.keys()
        user = self.users[user_name]
        for _, device in self.devices.iteritems():
            if user in device.users:
                device.users.remove(user)
        del self.users[user_name]

    def set_user_importance(self, user_name, element_name, value):
        assert element_name in self.elements.keys()
        assert user_name in self.users.keys()
        user = self.users[user_name]
        user.importance[element_name] = value

    def reset_all_user_importances(self):
        for _, user in self.users.iteritems():
            user.importance = {}

    def run(self, expect={}):
        """Run optimizer and print inputs and output. Optionally run tests on outputs."""
        elements, devices, users = self.elements.values(), self.devices.values(), self.users.values()
        output = optimize_device_assignment.optimize(elements, devices, users)

        print('\nInputs')
        print('=======\n')
        print('Users: ' + ', '.join([u.name for u in users]))
        print('')
        for element in elements:
            print(element)

        for device in devices:
            print(device)
            print('Users with access (%d): %s\n' % (len(device.users), ', '.join([user.name for user in device.users])))

        print('\nOutputs')
        print('=======\n')

        for device, elements in sorted(output.items()):
            print('%s <%d element(s) assigned>' % (device.name, len(elements)))
            for element in elements:
                print('> %s' % element)
            print('')

        # See if expectations fulfilled if specified previously
        if len(expect) > 0:
            msgs = []
            for device_name, element_names in expect.iteritems():
                assert device_name in self.devices.keys()
                device = self.devices[device_name]

                for element_name in element_names:
                    should_not = False
                    if element_name[0] == '~':
                        should_not = True
                        element_name = element_name[1:]
                    assert element_name in self.elements.keys()
                    element = self.elements[element_name]

                    if not should_not:
                        if element not in output[device]:
                            msgs += ['[FAIL] "%s" should be assigned to "%s".' % (element_name, device_name)]
                        else:
                            msgs += ['[SUCCESS] "%s" assigned to "%s" as expected.' % (element_name, device_name)]

                    if should_not:
                        if element in output[device]:
                            msgs += ['[FAIL] "%s" should not be assigned to "%s".' % (element_name, device_name)]
                        else:
                            msgs += ['[SUCCESS] "%s" not assigned to "%s" as expected.' % (element_name, device_name)]

            print('\nTESTS')
            print('=====\n')
            msgs.sort()
            for i, msg in enumerate(msgs):
                print('(%d) %s' % (i + 1, msg))
            print('')

            if any([msg.startswith('[FAIL') for msg in msgs]):
                raise Exception('Expectation(s) not met. Please check above.\n\n')


def get_properties_from_code(code):
    nums = [int(c) for c in code.strip()]
    return Properties(*nums)
