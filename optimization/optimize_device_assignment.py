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
    element_user_imp, element_device_imp, element_device_comp, user_device_access, \
    user_element_access = pre_process_objects(elements, devices, users)

    # Create empty model
    model = Model('device_assignment')
    model.params.LogToConsole = 0  # Uncomment to see logs in console

    # Add decision variables
    x = {}
    s = {}
    for e, element in enumerate(elements):
        for d, device in enumerate(devices):
            x[e, d] = model.addVar(vtype=GRB.BINARY,
                                   name='x_%s_%s' % (element.name, device.name))
            s[e, d] = model.addVar(vtype=GRB.SEMIINT,
                                   name='s_%s_%s' % (element.name, device.name))
    model.update()

    for d, device in enumerate(devices):
        # Constraint 1: sum of widget areas shouldn't exceed device capacity (area)
        model.addConstr(quicksum(s[e, d] * x[e, d] for e, _ in enumerate(elements)) <= device._area,
                        'capacity_constraint_%s' % device.name)

        # if np.any(user_device_access[:, d]):
        #     # Constraint 2: a device which is accessible by a user should have at least one element
        #     model.addConstr(quicksum(x[e, d] for e, _ in enumerate(elements)) >= 1,
        #                     'at_least_one_widget_constraint_%s' % device.name)
        # else:
        #     # Constraint 3: a device which is not accessible by any user should not have a element
        #     model.addConstr(quicksum(x[e, d] for e, _ in enumerate(elements)) == 0,
        #                     'no_widget_constraint_%s' % device.name)

        for e, element in enumerate(elements):
            # Constraint 4: the min. width/height of an element should not exceed device width/height
            model.addConstr(element.min_width * x[e, d] <= device.width,
                            'min_width_exceed_constraint_%s_on_%s' % (element.name, device.name))
            model.addConstr(element.min_height * x[e, d] <= device.height,
                            'min_height_exceed_constraint_%s_on_%s' % (element.name, device.name))

            # Constraint 5: Set s to zero if x is zero
            model.addGenConstrIndicator(x[e, d], False, s[e, d] == 0)
            model.addGenConstrIndicator(x[e, d], True, s[e, d] >= element._min_area)
            model.addGenConstrIndicator(x[e, d], True, s[e, d] <= min(element._max_area, device._area))

    model.update()

    # Do not assign zero-compatibility elements
    for d, device in enumerate(devices):
        for e, element in enumerate(elements):
            if element_device_comp[e, d] < 1e-4:
                model.addConstr(x[e, d] == 0,
                                name='zero_compatibility_%s_%s' % (element.name, device.name))
    model.update()

    # Make sure element privacy is respected.
    # All users must have access to a device as well as assigned elements.
    # That is, if there is even one user who is not authorised to view an element, the element
    # should not be assigned to the device.
    element_device_access = np.zeros((len(elements), len(devices)))
    for d, device in enumerate(devices):
        for e, element in enumerate(elements):
            if np.any(user_device_access[:, d] > user_element_access[:, e]):
                model.addConstr(x[e, d] == 0,
                                name='privacy_%s_%s' % (element.name, device.name))
            else:
                element_device_access[e, d] = 1

    model.update()

    # Diversity variables and constraints
    user_num_all_elements = {}
    user_num_unique_elements = {}
    user_num_element = {}
    user_num_replicated_elements = {}
    element_assigned_to_user = {}
    for u, user in enumerate(users):
        # Total number of elements that a user has access to (incl. duplicates)
        user_num_all_elements[u] = model.addVar(vtype=GRB.SEMIINT)
        model.addConstr(user_num_all_elements[u]
                        == quicksum(x[e, d] * user_device_access[u, d]
                                    for e, element in enumerate(elements)
                                       for d, device in enumerate(devices)))

        for e, element in enumerate(elements):
            # The number of a particular element a user has assigned
            user_num_element[u, e] = model.addVar(vtype=GRB.SEMIINT)
            element_assigned_to_user[e, u] = model.addVar(vtype=GRB.BINARY)  # bool for above
            model.addConstr(user_num_element[u, e]
                            == quicksum(x[e, d] * user_device_access[u, d]
                                        for d, device in enumerate(devices)))
            model.addGenConstrMin(element_assigned_to_user[e, u], [user_num_element[u, e], 1])

        # Number of unique elements assigned to user
        user_num_unique_elements[u] = model.addVar(vtype=GRB.SEMIINT)
        model.addConstr(user_num_unique_elements[u]
                        == quicksum(element_assigned_to_user[e, u]
                                    for e, element in enumerate(elements)))

        # Number of "redundant" element assignments (duplicates)
        user_num_replicated_elements[u] = model.addVar(vtype=GRB.SEMIINT)
        model.addConstr(user_num_replicated_elements[u]
                        == user_num_all_elements[u] - user_num_unique_elements[u])

    model.update()

    # Objective function
    cost = 0

    alpha = 1.3
    beta = 1.0
    gamma = 0.01
    delta = 0.1
    max_elements_per_device_guideline = 2

    # Maximize importance and compatibility
    cost += alpha * quicksum(
                element_device_imp[e, d] * element_device_comp[e, d] * element_device_access[e, d] * x[e, d]
                for e, _ in enumerate(elements)
                    for d, device in enumerate(devices)
            )

    # minimize (A_max - A) / A_max
    cost -= beta * quicksum(
                float(element_device_imp[e, d] * element_device_comp[e, d] * element_device_access[e, d])
                * (min(element._max_area, device._area) - s[e, d]) / min(element._max_area, device._area)
                * x[e, d]
                for e, element in enumerate(elements)
                    for d, device in enumerate(devices)
            )

    # Penalty for assigning duplicate/replicate elements
    cost -= gamma * quicksum(user_num_replicated_elements[u] / np.sum(user_element_access[u, :])
                             for u, user in enumerate(users))

    # Penalty for assigning too much on one device
    cost -= delta * quicksum(quicksum(x[e, d] for e, element in enumerate(elements))
                             / max_elements_per_device_guideline
                             for d, device in enumerate(devices))

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
        element._optimizer_size = s[e, d].x
        output[device].append(element)
    return output


def pre_process_objects(elements, devices, users):
    # compatibility_metric = 'distance'
    compatibility_metric = 'dot'

    num_elements = len(elements)
    num_devices = len(devices)
    num_users = len(users)

    # Add noise to prevent stalemates
    def add_noise(array):
        array += 1e-6 * np.random.random(size=array.shape)

    # Retrieve, store and normalize user-specific element importance
    element_user_imp = np.ones((num_elements, num_users))
    element_name_index = dict((element.name, i) for i, element in enumerate(elements))
    for u, user in enumerate(users):
        element_user_imp[:, u] = [element.importance for element in elements]
        for element_name, importance in user.importance.iteritems():
            element_user_imp[element_name_index[element_name], u] = importance
        element_user_imp[:, u] /= np.linalg.norm(element_user_imp[:, u])
    add_noise(element_user_imp)

    # Calculate and create normalized matrix of element-device compatibility
    element_device_comp = np.zeros((num_elements, num_devices))
    for d, device in enumerate(devices):
        for e, element in enumerate(elements):
            element_device_comp[e, d] = device.calculate_compatibility(element, compatibility_metric)
        element_device_comp[:, d] /= np.linalg.norm(element_device_comp[:, d])
    add_noise(element_device_comp)

    # Set boolean matrix of user-device access
    # TODO: try continuous numbers
    user_device_access = np.zeros((num_users, num_devices))
    for d, device in enumerate(devices):
        for user in device.users:
            user_device_access[users.index(user), d] = 1

    # Set boolean matrix of user-element access
    user_element_access = np.empty((num_users, num_elements))
    for e, element in enumerate(elements):
        for u, user in enumerate(users):
            user_element_access[u, e] = 1 if element.user_has_access(user) else 0

    # Normalize element importances per device
    element_device_imp = np.asmatrix(element_user_imp) * np.asmatrix(user_device_access)
    for d, device in enumerate(devices):
        norm = np.linalg.norm(element_device_imp[:, d])
        if norm > 0.0:
            element_device_imp[:, d] /= norm

    return element_user_imp, element_device_imp, element_device_comp, user_device_access, \
           user_element_access
