from element import Element
import optimize_layout

elements = [
    Element(name='video', type='', size=5, importance=10),
    Element(name='play',  type='', size=1, importance=9),
    Element(name='next',  type='', size=1, importance=2),
    Element(name='prev',  type='', size=1, importance=2),
]

print('inputs: %s' % [e.name for e in elements])
output = optimize_layout.optimize(elements)
print('outputs: %s' % [e.name for e in output])
