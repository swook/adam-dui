import converters
import optimize

web_input = '''
    {
      "devices": [
        {
          "deviceClass": "tablet",
          "capacity": 8
        },
        {
          "deviceClass": "smartphone",
          "capacity": 6
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

print('inputs: %s' % web_input)
elements, devices = converters.from_web(web_input)
print('output (elements): %s' % elements)
print('output (devices): %s' % devices)

our_output = optimize.optimize(elements, devices)

print('inputs: %s' % our_output)
print('output: %s' % converters.to_web(our_output))

