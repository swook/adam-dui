import json

import converters
import optimize

from user import User
from device import Device
from element import Element
from properties import Properties

'''
    Python inputs.
'''
alice = User(name='alice')
bob = User(name='bob')
caroline = User(name='caroline')
darryl = User(name='darryl')
users = [alice, bob, caroline, darryl]

alice.importance = {
    'video':    10,
    'play':     6,
    'next':     5,
    'prev':     5,
    'comments': 1,
}
bob.importance = {
    'video':    10,
    'play':     2,
    'next':     1,
    'prev':     1,
    'comments': 1,
}
caroline.importance = {
    'video':    10,
    'play':     10,
    'next':     10,
    'prev':     10,
    'comments': 1,
}
darryl.importance = {
    'video':    1,
    'play':     1,
    'next':     1,
    'prev':     1,
    'comments': 10,
}

# Define all elements and widgets
elements = [
    Element(
        name='video',
        importance=10,
        requirements=Properties(
            visual_display=5,
            text_input=0,
            touch_pointing=0,
            mouse_pointing=0,
        ),
        min_width=400,
        min_height=300,
        max_width=3200,
        max_height=1800,
    ),
    Element(
        name='play',
        importance=9,
        requirements=Properties(
            visual_display=1,
            text_input=0,
            touch_pointing=2,
            mouse_pointing=3,
        ),
        min_width=10,
        min_height=10,
        max_width=100,
        max_height=100,
    ),
    Element(
        name='next',
        importance=2,
        requirements=Properties(
            visual_display=1,
            text_input=0,
            touch_pointing=2,
            mouse_pointing=3,
        ),
        min_width=10,
        min_height=10,
        max_width=100,
        max_height=100,
    ),
    Element(
        name='prev',
        importance=2,
        requirements=Properties(
            visual_display=1,
            text_input=0,
            touch_pointing=2,
            mouse_pointing=3,
        ),
        min_width=10,
        min_height=10,
        max_width=100,
        max_height=100,
    ),
    Element(
        name='comments',
        importance=5,
        requirements=Properties(
            visual_display=3,
            text_input=5,
            touch_pointing=1,
            mouse_pointing=3,
        ),
        min_width=160,
        min_height=50,
        max_width=1000,
        max_height=2000,
    ),
]

# Define devices and users who can access devices
devices = [
    Device(
        name='TV',
        width=1600,
        height=1200,
        affordances=Properties(
            visual_display=5,
            text_input=0,
            touch_pointing=0,
            mouse_pointing=0,
        ),
        users=[alice, bob, caroline, darryl],
    ),
    Device(
        name='Darryl\'s PC',
        width=1280,
        height=800,
        affordances=Properties(
            visual_display=4,
            text_input=5,
            touch_pointing=0,
            mouse_pointing=5,
        ),
        users=[caroline, darryl],
    ),
    Device(
        name='Tablet',
        width=1024,
        height=800,
        affordances=Properties(
            visual_display=3,
            text_input=3,
            touch_pointing=4,
            mouse_pointing=0,
        ),
        users=[alice, bob, caroline, darryl],
    ),
    Device(
        name='Caroline\'s Phone',
        width=400,
        height=900,
        affordances=Properties(
            visual_display=2,
            text_input=2,
            touch_pointing=3,
            mouse_pointing=0,
        ),
        users=[caroline],
    ),
    Device(
        name='Alice\'s Watch',
        width=300,
        height=300,
        affordances=Properties(
            visual_display=1,
            text_input=1,
            touch_pointing=1,
            mouse_pointing=0,
        ),
        users=[alice],
    ),
    Device(
        name='Bob\'s Watch',
        width=300,
        height=300,
        affordances=Properties(
            visual_display=1,
            text_input=1,
            touch_pointing=1,
            mouse_pointing=0,
        ),
        users=[bob],
    ),
    Device(
        name='Abandoned Computer',
        width=1280,
        height=720,
        affordances=Properties(
            visual_display=3,
            text_input=5,
            touch_pointing=0,
            mouse_pointing=4,
        ),
        users=[],
    ),
]

our_inputs_json = converters.our_inputs_to_json(elements, devices, users)
print("GENERATED JSON")
print("==============")
print(our_inputs_json)

# Add token for Roman
token = 'something'
intermediate= json.loads(our_inputs_json)
intermediate['token'] = token
our_inputs_json = json.dumps(intermediate, indent=2, sort_keys=True)

print('')
print('RECOVERED FROM JSON')
print('===================')
elements, devices, users, token = converters.json_to_our_inputs(our_inputs_json)
print('Elements:')
for element in elements:
    print(element)
print('\nDevices:')
for device in devices:
    print(device)
print('\nUsers:')
for user in users:
    print(user)

# Make sure we don't lose information when converting between JSON and Python representations.
assert our_inputs_json == converters.our_inputs_to_json(elements, devices, users, token=token)

print('')
print('OPTIMIZER')
print('=========')
our_output_json = optimize.handle_web_input(our_inputs_json)

print('')
print('OPTIMIZER OUTPUT IN JSON')
print('========================')
print(our_output_json)
