import json

from device import Device
from element import Element

'''
Input:
    JSON document
    {
      "devices": [
        {
          "deviceClass": "tablet",
          "capacity": 8
        },
        {
          "deviceClass": "smartphone",
          "capacity": 6
        },
        {
          "deviceClass": "tv",
          "capacity": 15
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

Output:
    List of elements and devices
'''
def from_web(web_input):
    web_input = json.loads(web_input)

    devices = []
    for web_device in web_input['devices']:
        devices.append(
            Device(
                name=web_device['deviceClass'],
                capacity=int(web_device['capacity']),
            )
        )

    elements = []
    for web_element in web_input['elements']:
        elements.append(
            Element(
                name=web_element['name'],
                type='',
                size=int(web_element['size']),
                importance=int(web_element['importance']),
            )
        )

    return elements, devices



'''
Input:
    Map of device class to list of elements

Output:
    JSON document
    {
        "tablet": ["video", "play", "prev", "next"],
        "smartphone": ["play", "prev", "next"]
    }
'''
def to_web(our_output):
    output = {}
    for device_class, elements in our_output.items():
        output[device_class] = [e.name for e in elements]
    return json.dumps(output).decode('utf-8')
