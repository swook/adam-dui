from gurobipy import *

'''


Input:
    elements (list of Element)

Output:
    list of Element
'''
def optimize(elements):
    n = len(elements)
    positions = list(range(n))

    # Create empty model
    model = Model('linear_layout')

    # Add decision variables
    x = {}
    for e in elements:
        for j in positions:
            x[(e, j)] = model.addVar(vtype=GRB.BINARY, name='%s_%d' % (e.name, j))
    model.update()

    # Constraint 1: each element is assigned once
    for e in elements:
        model.addConstr(quicksum(x[(e, j)] for j in range(n)) == 1,
                        'uniqueness_constraint_%s' % e.name)

    # Constraint 2: each slot has one assignment
    for j in positions:
        model.addConstr(quicksum(x[(e, j)] for e in elements) == 1,
                        'uniqueness_constraint_%d' % j)
    model.update()

    # Objective function
    cost = quicksum(e.importance * (j + 1) * x[(e, j)]
                    for e in elements
                        for j in positions)
    model.setObjective(cost, GRB.MINIMIZE)

    # Solve
    model.optimize()

    # Create output list of elements (sorted)
    output = [None] * n  # Create None list of size n
    for key, var in x.items():
        if var.x != 1:  # Ignore if not 1.0 (assignment)
            continue
        element, index = key
        output[index] = element

    return output
