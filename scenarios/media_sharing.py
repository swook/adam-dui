# flake8: noqa
from common import *

# Name | Importance | min W | min H | max W | max H | Properties
# Properties: visual_display, text_input, touch_pointing, mouse_pointing
element_definitions = {
    'video':             'video             | 10 | 500 | 300 | 2600 | 2000 | 5000',
    'playback controls': 'playback controls |  8 | 150 | 100 |  500 |  300 | 0032',
    'suggestions':       'suggestions       |  5 | 500 | 600 | 1000 | 1000 | 3054',
    'comments':          'comments          |  4 | 500 | 900 |  800 | 1500 | 1500',
    'volume controls':   'volume controls   |  2 | 150 | 100 |  500 |  300 | 0032',
}
# Name | Width | Height | Properties | Users
# Properties: visual_display, text_input, touch_pointing, mouse_pointing
device_definitions = {
    'TV':               'TV               | 2600 | 1600 | 5000 | alice,bob,caroline,darryl',
    'PC':               'PC               | 1920 | 1080 | 3505 | alice,bob,caroline,darryl',
    'Laptop':           'Laptop           | 1280 |  800 | 3403 | alice,bob,caroline,darryl',
    'Tablet':           'Tablet           | 1280 |  720 | 3250 | alice,bob,caroline,darryl',
    'Phone (Alice)':    'Phone (Alice)    |  400 |  900 | 0330 | alice',
    'Phone (Caroline)': 'Phone (Caroline) |  400 |  900 | 0330 | caroline',
    'Watch (Alice)':    'Watch (Alice)    |  150 |  150 | 0020 | alice',
    'Watch (Bob)':      'Watch (Bob)      |  150 |  150 | 0020 | bob',
    'Abandoned PC':     'Abandoned PC     | 1024 |  900 | 3505 |',
}
def init(test_name):
    scenario = Scenario(test_name)
    scenario.add_users_by_names('alice', 'bob', 'caroline', 'darryl')
    return scenario
def pick(definitions, keys):
    return '\n'.join([definitions[key] for key in keys if key in definitions.keys()])

#########
# TEST 1: An "Abandoned PC" which is accessible by no users
#         should have none of the elements assigned.
# Keywords: User Access
###########
scenario = init('Abandoned PC should have no elements.')
scenario.add_elements_from_text(pick(element_definitions,
    ['video', 'playback controls', 'volume controls', 'comments', 'suggestions']))
scenario.add_devices_from_text(pick(device_definitions,
    ['Abandoned PC']))
scenario.run(expect={
    'Abandoned PC': ['~video', '~playback controls', '~volume controls', '~comments', '~suggestions'],
})


#########
# TEST 2: If the "playback controls" element is private to
#         "alice", it should not be accessible by other users.
# Keywords: Element Privacy, User Access
###########
scenario = init('Private "playback controls" should not be accessible by other users.')
scenario.add_elements_from_text(pick(element_definitions,
    ['video', 'playback controls', 'volume controls', 'comments', 'suggestions']))
scenario.elements['playback controls'].user_give_access(scenario.users['alice'])
scenario.add_devices_from_text(pick(device_definitions,
    ['TV', 'PC', 'Tablet', 'Phone (Alice)', 'Phone (Caroline)', 'Watch (Alice)', 'Watch (Bob)']))
scenario.run(expect={
    'TV':               ['~playback controls'],
    'PC':               ['~playback controls'],
    'Tablet':           ['~playback controls'],
    'Phone (Caroline)': ['~playback controls'],
    'Watch (Bob)':      ['~playback controls'],
})


#########
# TEST 3: If only a laptop is available, most important elements
#         should be assigned to it.
# Keywords: Element Diversity
###########
scenario = init('With only a laptop available, most important elements should be assigned.')
scenario.add_elements_from_text(pick(element_definitions,
    ['video', 'playback controls', 'volume controls', 'comments', 'suggestions']))
scenario.add_devices_from_text(pick(device_definitions,
    ['Laptop']))
scenario.run(expect={
    'Laptop': ['video', 'playback controls', 'suggestions'],
})


#########
# TEST 4: If both TV and PC are available, comments should only
#         appear on the PC.
# Keywords: Element Compatibility
###########
scenario = init('If both TV and PC available, comments should only be on PC.')
scenario.add_elements_from_text(pick(element_definitions,
    ['video', 'playback controls', 'volume controls', 'comments']))
scenario.add_devices_from_text(pick(device_definitions,
    ['TV', 'PC']))
scenario.run(expect={
    'TV': ['~comments', 'video'],
    'PC': ['comments'],
})


#########
# TEST 5: With all devices and elements, we expect the "video" to be on the TV,
#         "comments" on the PC, and "playback controls" on all phones.
# Keywords: Element Compatibility
###########
scenario = init('Various compatibilities.')
scenario.add_elements_from_text(pick(element_definitions,
    ['video', 'playback controls', 'volume controls', 'comments', 'suggestions']))
scenario.add_devices_from_text(pick(device_definitions,
    ['TV', 'PC', 'Tablet', 'Phone (Alice)', 'Phone (Caroline)', 'Watch (Alice)', 'Watch (Bob)']))
scenario.run(expect={
    'TV':               ['video', '~playback controls', '~volume controls', '~comments', '~suggestions'],
    'PC':               ['comments'],
    'Tablet':           ['suggestions'],
    'Phone (Alice)':    ['volume controls'],
    #'Phone (Caroline)': ['playback controls'],
    'Watch (Alice)':    ['playback controls'],
    'Watch (Bob)':      ['playback controls'],
})

check_previous_tests_for_failure()
