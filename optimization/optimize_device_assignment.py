from gurobipy import *
import numpy as np


def preprocess(elements, devices, users):
    pass


'''

Input:
    elements (list of Element)
    devices (list of Device)
    users (list of User)

Output:
    dict (device_class => list of Element)
    {
        'tv': [Element1, Element2],
        'phone': [Element1, Element3],
        'watch': [Element1],
    }
'''
def optimize(elements, devices, users):
    n = len(elements)
    m = len(devices)

    # Create empty model
    model = Model('device_assignment')

    # Add decision variables
    x = {}
    for e in elements:
        for d in devices:
            x[(e, d)] = model.addVar(vtype=GRB.BINARY, name='%s_%s' % (e.name, d.name))
    model.update()

    # Constraint 1: sum of element sizes don't exceed device class capacity
    for d in devices:
        model.addConstr(quicksum(e.size * x[(e, d)] for e in elements) <= d.capacity,
                        'capacity_constraint_%s' % d.name)

    # Constraint 2: a device class should have at least one element assigned
    for d in devices:
        model.addConstr(quicksum(x[(e, d)] for e in elements) >= 1,
                        'device_has_some_elements_constraint_%s' % d.name)

    # Constraint 3: show element at least once
    for e in elements:
        model.addConstr(quicksum(x[(e, d)] for d in devices) >= 1,
                        'element_at_least_once_constraint_%s' % e.name)
    model.update()

    # Objective function
    cost = quicksum(e.importance * x[(w, e, d)]
                    for e in elements
                        for d in devices)
    model.setObjective(cost, GRB.MAXIMIZE)

    # Solve
    model.optimize()
    if model.status != GRB.status.OPTIMAL:
        return None

    # Create output list of elements (sorted)
    output = {}
    for key, var in x.items():
        if var.x != 1:  # Ignore if not 1.0 (assignment)
            continue
        element, device = key
        if device.name not in output:
            output[device.name] = []
        output[device.name].append(element)

    return output
