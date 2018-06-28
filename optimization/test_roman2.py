import optimize

input_json = """
{
  "data": {
    "devices": [
      {
        "__class__": "Device",
        "name": "Bobby's TV",
        "width": 1920,
        "height": 1080,
        "users": [
          "bobby:github"
        ],
        "affordances": {
          "__class__": "Properties",
          "visual_display": 5,
          "text_input": 0,
          "mouse_pointing": 0,
          "touch_pointing": 0
        }
      },
      {
        "__class__": "Device",
        "name": "Bobby's Tablet",
        "width": 1440,
        "height": 1024,
        "users": [
          "bobby:github"
        ],
        "affordances": {
          "__class__": "Properties",
          "visual_display": 3,
          "text_input": 3,
          "mouse_pointing": 0,
          "touch_pointing": 5
        }
      },
      {
        "__class__": "Device",
        "name": "Bobby's Smartphone",
        "width": 400,
        "height": 667,
        "users": [
          "bobby:github"
        ],
        "affordances": {
          "__class__": "Properties",
          "visual_display": 2,
          "text_input": 2,
          "mouse_pointing": 0,
          "touch_pointing": 4
        }
      },
      {
        "__class__": "Device",
        "name": "Bobby's Smartwatch",
        "width": 312,
        "height": 390,
        "users": [
          "bobby:github"
        ],
        "affordances": {
          "__class__": "Properties",
          "visual_display": 1,
          "text_input": 1,
          "mouse_pointing": 0,
          "touch_pointing": 2
        }
      }
    ],
    "elements": [
      {
        "__class__": "Element",
        "name": "whiteboard",
        "importance": 15,
        "allowed_users": ["raedle:github", "bobby:github"],
        "requirements": {
          "__class__": "Properties",
          "visual_display": 5,
          "text_input": 0,
          "mouse_pointing": 3,
          "touch_pointing": 3
        },
        "min_width": 400,
        "min_height": 400,
        "max_width": 2000,
        "max_height": 2000
      },
      {
        "__class__": "Element",
        "name": "colors",
        "importance": 1,
        "allowed_users": ["raedle:github", "bobby:github"],
        "requirements": {
          "__class__": "Properties",
          "visual_display": 2,
          "text_input": 0,
          "mouse_pointing": 1,
          "touch_pointing": 4
        },
        "min_width": 400,
        "min_height": 40,
        "max_width": 800,
        "max_height": 40
      },
      {
        "__class__": "Element",
        "name": "brushes",
        "importance": 1,
        "allowed_users": ["raedle:github", "bobby:github"],
        "requirements": {
          "__class__": "Properties",
          "visual_display": 3,
          "text_input": 0,
          "mouse_pointing": 2,
          "touch_pointing": 3
        },
        "min_width": 400,
        "min_height": 40,
        "max_width": 800,
        "max_height": 40
      }
    ],
    "users": [
      {
        "__class__": "User",
        "id": "raedle:github",
        "name": "raedle"
      },
      {
        "__class__": "User",
        "id": "bobby:github",
        "name": "bobby",
        "element_importances": {
            "brushes": 2,
            "colors": 0
        }
      }
    ]
  },
  "token": "blah"
}
"""

output_json = optimize.handle_web_input(input_json)
print(output_json)
