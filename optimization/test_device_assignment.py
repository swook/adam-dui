import random
import optimize_device_assignment
from element import Element
from device import Device


elements = [
    Element(name='video', type='', size=5, importance=10),
    Element(name='play',  type='', size=1, importance=9),
    Element(name='next',  type='', size=1, importance=2),
    Element(name='prev',  type='', size=1, importance=2),
]
random.shuffle(elements)

devices = [
    Device(name='tv', capacity=6),
    Device(name='pc', capacity=4),
    Device(name='tablet', capacity=3),
    Device(name='phone', capacity=2)
]


output = optimize_device_assignment.optimize(elements, devices)

print('inputs: %s' % [e.name for e in elements])
print('outputs: %s' % [e.name for e in output])
