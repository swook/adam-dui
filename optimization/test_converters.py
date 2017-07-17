import converters
import optimize

from user import User
from device import Device
from widget import Widget
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
    'play':     1,
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
        name='TV',
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
    Device(
        name='Abandoned Computer',
        capacity=5,
        affordances=Properties(
            visual_display=3,
            text_input=5,
            touch_pointing=0,
            mouse_pointing=4,
        ),
        users=[],
    ),
]

web_input = '''
    {
      "devices": [
        {
          "name": "TV",
          "capacity": 15,
          "affordances": {
            "visual_display": 5
          },
          "users": ["alice", "bob", "caroline", "darryl"]
        },
        {
          "name": "Darryl's PC",
          "capacity": 8,
          "affordances": {
            "visual_display": 4,
            "text_input": 5,
            "mouse_pointing": 5
          },
          "users": ["caroline", "darryl"]
        },
        {
          "name": "Tablet",
          "capacity": 4,
          "affordances": {
              "visual_display": 3,
              "text_input": 3,
              "touch_pointing": 4
          },
          "users": ["alice", "bob", "caroline", "darryl"]
        },
        {
          "name": "Caroline's Phone",
          "capacity": 2,
          "affordances": {
              "visual_display": 2,
              "text_input": 2,
              "touch_pointing": 3,
              "mouse_pointing": 0
          },
          "users": ["caroline"]
        },
        {
          "name": "Alice's Watch",
          "capacity": 1,
          "affordances": {
              "visual_display": 1,
              "text_input": 1,
              "touch_pointing": 1,
              "mouse_pointing": 0
          },
          "users": ["alice"]
        },
        {
          "name": "Bob's Watch",
          "capacity": 1,
          "affordances": {
              "visual_display": 1,
              "text_input": 1,
              "touch_pointing": 1,
              "mouse_pointing": 0
          },
          "users": ["bob"]
        },
        {
          "name": "Abandoned Computer",
          "capacity": 5,
          "affordances": {
              "visual_display": 3,
              "text_input": 5,
              "touch_pointing": 0,
              "mouse_pointing": 4
          },
          "users": []
        }
      ],
      "elements": [
        {
          "name": "video",
          "size": 10,
          "importance": 10
        },
        {
          "name": "play",
          "size": 1,
          "importance": 9
        },
        {
          "name": "next",
          "size": 1,
          "importance": 2
        },
        {
          "name": "prev",
          "size": 1,
          "importance": 2
        }
      ]
    }
'''

our_inputs_json = converters.our_inputs_to_json(elements, devices, users)
print("GENERATED JSON")
print("==============")
print(our_inputs_json)

print('')
print('RECOVERED FROM JSON')
print('===================')
elements, devices, users = converters.json_to_our_inputs(our_inputs_json)
print('Elements:')
for element in elements:
    print(element)
print('\nDevices:')
for device in devices:
    print(device)
print('\nUsers:')
for user in users:
    print(user)

print('')
print('OPTIMIZER')
print('=========')
our_output_json = optimize.handle_web_input(our_inputs_json)

print('')
print('OPTIMIZER OUTPUT IN JSON')
print('========================')
print(our_output_json)
