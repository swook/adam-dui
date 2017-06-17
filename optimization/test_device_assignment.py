import random
import optimize_device_assignment
from element import Element
from device import Device


elements = [
    Element(name='video', type='', size=5, importance=10),
    Element(name='play',  type='', size=1, importance=9),
    Element(name='next',  type='', size=1, importance=2),
    Element(name='prev',  type='', size=1, importance=2),
    Element(name='comments', type='', size=3, importance=5),
]
# random.shuffle(elements)

devices = [
    Device(name='tv', capacity=15),
    Device(name='pc', capacity=8),
    Device(name='tablet', capacity=4),
    Device(name='phone', capacity=2),
    Device(name='watch', capacity=1),
]


output = optimize_device_assignment.optimize(elements, devices)

print('\ninputs: %s' % [e.name for e in elements])
for key, elements in output.items():
    print('outputs[%s]: %s' % (key, [e.name for e in elements]))
