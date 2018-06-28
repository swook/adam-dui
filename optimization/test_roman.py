import converters
import optimize

from user import User
from device import Device
from widget import Widget
from element import Element
from properties import Properties

roman_json = """
{
  "devices": [
    {
      "__class__": "Device",
      "affordances": {
        "__class__": "Properties",
        "mouse_pointing": 5,
        "text_input": 4,
        "touch_pointing": 3,
        "visual_display": 5
      },
      "capacity": 15,
      "name": "TV",
      "users": [
        "raedle:github"
      ]
    }
  ],
  "elements": [
    {
      "__class__": "Element",
      "name": "video",
      "importance": 10,
      "widgets": [
        {
          "__class__": "Widget",
          "size": 10,
          "visual_quality": 3,
          "requirements": {
            "__class__": "Properties",
            "mouse_pointing": 0,
            "text_input": 0,
            "touch_pointing": 0,
            "visual_display": 5
          }
        }
      ]
    },
    {
      "__class__": "Element",
      "name": "play",
      "importance": 9,
      "widgets": [
        {
          "__class__": "Widget",
          "size": 1,
          "visual_quality": 1,
          "requirements": {
            "__class__": "Properties",
            "mouse_pointing": 3,
            "text_input": 0,
            "touch_pointing": 2,
            "visual_display": 1
          }
        }
      ]
    },
    {
      "__class__": "Element",
      "name": "next",
      "importance": 2,
      "widgets": [
        {
          "__class__": "Widget",
          "size": 1,
          "visual_quality": 1,
          "requirements": {
            "__class__": "Properties",
            "mouse_pointing": 3,
            "text_input": 0,
            "touch_pointing": 2,
            "visual_display": 1
          }
        }
      ]
    },
    {
      "__class__": "Element",
      "name": "prev",
      "importance": 2,
      "widgets": [
        {
          "__class__": "Widget",
          "size": 1,
          "visual_quality": 1,
          "requirements": {
            "__class__": "Properties",
            "mouse_pointing": 3,
            "text_input": 0,
            "touch_pointing": 2,
            "visual_display": 1
          }
        }
      ]
    },
    {
      "__class__": "Element",
      "name": "comments",
      "importance": 3,
      "widgets": [
        {
          "__class__": "Widget",
          "size": 5,
          "visual_quality": 1,
          "requirements": {
            "__class__": "Properties",
            "mouse_pointing": 3,
            "text_input": 5,
            "touch_pointing": 1,
            "visual_display": 3
          }
        }
      ]
    }
  ],
  "users": [
    {
      "__class__": "User",
      "id": "raedle:github",
      "name": "raedle"
    }
  ]
}
"""


print('')
print('RECOVERED FROM JSON')
print('===================')
elements, devices, users = converters.json_to_our_inputs(roman_json)
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
our_output_json = optimize.handle_web_input(roman_json)

print('')
print('OPTIMIZER OUTPUT IN JSON')
print('========================')
print(our_output_json)
