import random

from properties import Properties
from element import Element
from widget import Widget
from device import Device
from user import User
import optimize_device_assignment

# Define all users
alice    = User(name='alice')
bob      = User(name='bob')
caroline = User(name='caroline')
darryl   = User(name='darryl')
users = [alice, bob, caroline, darryl]

# Define all elements and widgets
elements = [
    Element(
        name='video',
        importance=10,
        widgets=[
            Widget(
                size=10,
                visual_quality=3,
                requirements=Properties(
                    visual_display=5,
                    text_input=0,
                    touch_pointing=0,
                    mouse_pointing=0,
                ),
            ),
        ],
    ),
    Element(
        name='play',
        importance=9,
        widgets=[
            Widget(
                size=1,
                visual_quality=1,
                requirements=Properties(
                    visual_display=1,
                    text_input=0,
                    touch_pointing=2,
                    mouse_pointing=3,
                ),
            ),
            Widget(
                size=3,
                visual_quality=2,
                requirements=Properties(
                    visual_display=1,
                    text_input=0,
                    touch_pointing=4,
                    mouse_pointing=3,
                ),
            ),
        ],
    ),
    Element(
        name='next',
        importance=2,
        widgets=[
            Widget(
                size=1,
                visual_quality=1,
                requirements=Properties(
                    visual_display=1,
                    text_input=0,
                    touch_pointing=2,
                    mouse_pointing=3,
                ),
            ),
        ],
    ),
    Element(
        name='prev',
        importance=2,
        widgets=[
            Widget(
                size=1,
                visual_quality=1,
                requirements=Properties(
                    visual_display=1,
                    text_input=0,
                    touch_pointing=2,
                    mouse_pointing=3,
                ),
            ),
        ],
    ),
    Element(
        name='comments',
        importance=5,
        widgets=[
            Widget(
                size=5,
                visual_quality=1,
                requirements=Properties(
                    visual_display=3,
                    text_input=5,
                    touch_pointing=1,
                    mouse_pointing=3,
                ),
            ),
        ],
    ),
]

# Define devices and users who can access devices
devices = [
    Device(
        name='tv',
        capacity=15,
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
        capacity=8,
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
        capacity=4,
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
        capacity=2,
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
        capacity=1,
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
        capacity=1,
        affordances=Properties(
            visual_display=1,
            text_input=1,
            touch_pointing=1,
            mouse_pointing=0,
        ),
        users=[bob],
    ),
]

output = optimize_device_assignment.optimize(elements, devices, users)

print('\ninputs: %s' % [e.name for e in elements])
for key, elements in output.items():
    print('outputs[%s]: %s' % (key, [e.name for e in elements]))
