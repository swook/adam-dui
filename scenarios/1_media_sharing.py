# flake8: noqa
from common import *

element_definitions = {
    'video':             'video             | 15 | 500 | 300 | 2000 | 2000 | 5000',
    'playback controls': 'playback controls |  9 | 150 | 100 |  800 |  500 | 1023',
    'volume controls':   'volume controls   |  2 | 150 | 100 |  800 |  500 | 1023',
    'comments':          'comments          |  5 | 300 | 400 |  700 | 1200 | 1524',
    'suggestions':       'suggestions       |  5 | 300 | 600 |  700 | 1000 | 3043',
}
device_definitions = {
    'TV':               'TV               | 1920 | 1600 | 5000 | alice,bob,caroline,darryl',
    'PC':               'PC               | 1920 | 1080 | 4505 | alice,bob,caroline,darryl',
    'Tablet':           'Tablet           | 1280 |  720 | 4250 | alice,bob,caroline,darryl',
    'Phone (Alice)':    'Phone (Alice)    |  600 |  900 | 2340 | alice',
    'Phone (Caroline)': 'Phone (Caroline) |  600 |  900 | 2340 | caroline',
    'Watch (Alice)':    'Watch (Alice)    |  150 |  150 | 1010 | alice',
    'Watch (Bob)':      'Watch (Bob)      |  150 |  150 | 1010 | bob',
    'Abandoned PC':     'Abandoned PC     | 1024 |  900 | 4505 |',
}
def init():
    scenario = Scenario()
    scenario.add_users_by_names('alice', 'bob', 'caroline', 'darryl')
    return scenario
def pick(definitions, keys):
    return '\n'.join([definitions[key] for key in keys if key in definitions.keys()])

#########
# TEST 1: An "Abandoned PC" which is accessible by no users
#         should have none of the elements assigned.
# Keywords: User Access
###########
scenario = init()
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
scenario = init()
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
scenario = init()
scenario.add_elements_from_text(pick(element_definitions,
    ['video', 'playback controls', 'volume controls', 'comments', 'suggestions']))
scenario.add_devices_from_text(pick(device_definitions,
    ['PC']))
scenario.run(expect={
    'PC': ['video', 'comments', 'playback controls'],
})


#########
# TEST 4: If both TV and PC are available, comments should only
#         appear on the PC.
# Keywords: Element Compatibility
###########
scenario = init()
scenario.add_elements_from_text(pick(element_definitions,
    ['video', 'playback controls', 'volume controls', 'comments', 'suggestions']))
scenario.add_devices_from_text(pick(device_definitions,
    ['TV', 'PC']))
scenario.run(expect={
    'TV': ['~comments'],
    'PC': ['comments'],
})
