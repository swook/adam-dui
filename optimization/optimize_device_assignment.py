# flake8: noqa
from gurobipy import *
import numpy as np


def optimize(elements, devices, users):
    """Perform assignment of elements to devices.

    Input:
        elements (list of Element)
        devices (list of Device)
        users (list of User)

    Output:
        dict (Device => list of Element)
        {
            Device1: [Element1, Element2],
            Device2: [Element1, Element3],
            Device3: [Element1],
        }
    """
    element_device_imp, user_device_acc = pre_process_objects(elements, devices, users)

    # Create empty model
    model = Model('device_assignment')

    # Add decision variables
    x = {}
    a = {}
    for e, element in enumerate(elements):
        for d, device in enumerate(devices):
            x[e, d] = model.addVar(vtype=GRB.BINARY,
                                   name='x_%s_%s' % (element.name, device.name))
            a[e, d] = model.addVar(vtype=GRB.SEMIINT,
                                   lb=element._min_area, ub=min(element._max_area, device._area),
                                   name='a_%s_%s' % (element.name, device.name))
    model.update()

    for d, device in enumerate(devices):
        # Constraint 1: sum of widget areas shouldn't exceed device capacity (area)
        model.addConstr(quicksum(a[e, d] * x[e, d] for e, _ in enumerate(elements)) <= device._area,
                        'capacity_constraint_%s' % device.name)

        if np.any(user_device_acc[:, d]):
            # Constraint 2: a device which is accessible by a user should have at least one widget
            model.addConstr(quicksum(x[e, d] for e, _ in enumerate(elements)) >= 1,
                            'at_least_one_widget_constraint_%s' % device.name)
        else:
            # Constraint 3: a device which is not accessible by any user should not have a widget
            model.addConstr(quicksum(x[e, d] for e, _ in enumerate(elements)) == 0,
                            'no_widget_constraint_%s' % device.name)

        for e, element in enumerate(elements):
            # Constraint 4: the min. width/height of an element should not exceed device width/height
            model.addConstr(element.min_width * x[e, d] <= device.width,
                            'min_width_exceed_constraint_%s_on_%s' % (element.name, device.name))
            model.addConstr(element.min_height * x[e, d] <= device.height,
                            'min_height_exceed_constraint_%s_on_%s' % (element.name, device.name))

            # Constraint 5: Set a to zero if x is zero
            model.addGenConstrIndicator(x[e, d], False, a[e, d] == 0)

    model.update()

    # Objective function
    cost = 0

    alpha = 1.0
    beta = 1.0
    gamma = 0.0

    # Maximize importance and compatibility
    cost += alpha * quicksum(
                element_device_imp[e, d] * x[e, d]
                for e, _ in enumerate(elements)
                    for d, device in enumerate(devices)
            )

    # minimize (A_max - A) / A_max
    cost -= beta * quicksum(
                (min(element._max_area, device._area) - a[e, d]) / min(element._max_area, device._area) * x[e, d]
                for e, element in enumerate(elements)
                    for d, device in enumerate(devices)
            )

    # Penalty term for assigning many elements on a device
    cost -= gamma * quicksum(x[e, d]
                for e, element in enumerate(elements)
                    for d, device in enumerate(devices)
            )

    model.setObjective(cost, GRB.MAXIMIZE)

    # Create output list of elements (sorted)
    output = {}
    for device in devices:
        output[device] = []

    # Solve
    model.optimize()
    if model.status != GRB.status.OPTIMAL:
        return output

    # Fill output with optimizer result
    for key, var in x.items():
        if var.x != 1:  # Ignore if not 1.0 (assignment)
            continue
        e, d = key

        element = elements[e]
        device = devices[d]
        output[device].append(element)
    return output


def pre_process_objects(elements, devices, users):
    # compatibility_metric = 'distance'
    compatibility_metric = 'dot'

    num_elements = len(elements)
    num_devices = len(devices)
    num_users = len(users)

    # Retrieve, store and normalize user-specific element importance
    element_user_imp = np.ones((num_elements, num_users))
    element_name_index = dict((element.name, i) for i, element in enumerate(elements))
    for u, user in enumerate(users):
        element_user_imp[:, u] = [element.importance for element in elements]
        for element_name, importance in user.importance.iteritems():
            element_user_imp[element_name_index[element_name], u] = importance
        element_user_imp[:, u] /= np.linalg.norm(element_user_imp[:, u])

    # Calculate and create normalized matrix of element-device compatibility
    element_device_comp = np.zeros((num_elements, num_devices))
    for d, device in enumerate(devices):
        for e, element in enumerate(elements):
            element_device_comp[e, d] = device.calculate_compatibility(element, compatibility_metric)
        element_device_comp[:, d] /= np.linalg.norm(element_device_comp[:, d])

    # Set boolean matrix of user-device access
    # TODO: try continuous numbers
    user_device_acc = np.zeros((num_users, num_devices))
    for d, device in enumerate(devices):
        for user in device.users:
            user_device_acc[users.index(user), d] = 1

    # Normalize element importances per device
    element_device_imp = np.multiply(element_device_comp, np.asarray(np.asmatrix(element_user_imp) * np.asmatrix(user_device_acc)))
    for d, device in enumerate(devices):
        norm = np.linalg.norm(element_device_imp[:, d])
        if norm > 1e-4:
            element_device_imp[:, d] /= norm

    return element_device_imp, user_device_acc
