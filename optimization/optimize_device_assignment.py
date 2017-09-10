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
        # (7) sum of widget areas shouldn't exceed device capacity (area)
        model.addConstr(quicksum(s[e, d] * x[e, d] for e, _ in enumerate(elements)) <= device._area,
                        'capacity_constraint_%s' % device.name)

        for e, element in enumerate(elements):
            # (8,9) the min. width/height of an element should not exceed device width/height
            model.addConstr(element.min_width * x[e, d] <= device.width,
                            'min_width_exceed_constraint_%s_on_%s' % (element.name, device.name))
            model.addConstr(element.min_height * x[e, d] <= device.height,
                            'min_height_exceed_constraint_%s_on_%s' % (element.name, device.name))

            # (10,11) Set s to zero if x is zero
            model.addGenConstrIndicator(x[e, d], False, s[e, d] == 0)
            model.addGenConstrIndicator(x[e, d], True, s[e, d] >= element._min_area)
            model.addGenConstrIndicator(x[e, d], True, s[e, d] <= min(element._max_area, device._area))

    model.update()

    # Make sure element privacy is respected.
    # All users must have access to a device as well as assigned elements.
    # That is, if there is even one user who is not authorised to view an element, the element
    # should not be assigned to the device.
    element_device_access = np.zeros((len(elements), len(devices)))
    for d, device in enumerate(devices):
        for e, element in enumerate(elements):
            # (13) user has no access to element so don't assign to user's device
            # (14) if zero compatibility element should not be placed on device
            not_accessible = np.any(user_device_access[:, d] > user_element_access[:, e]) or \
                             not np.any(user_device_access[:, d])
            if not_accessible or element_device_comp[e, d] < 1e-5:
                if element.name == 'Presentation (Notes)':
                    print('No %s on %s.' % (element.name, device.name))
                model.addConstr(x[e, d] == 0,
                                name='privacy_%s_%s' % (element.name, device.name))
            elif not not_accessible:
                element_device_access[e, d] = 1

    model.update()


    for d, device in enumerate(devices):
        if np.any(element_device_access[:, d]):
            # (12) a device which is accessible by a user should have at least one element
            min_size_check = np.zeros((len(elements), 1))
            for e, element in enumerate(elements):
                if element_device_access[e, d]:
                    min_size_check[e] = device.width >= element.min_width and \
                                        device.height >= element.min_height
            if np.any(min_size_check):
                model.addConstr(quicksum(x[e, d] for e, _ in enumerate(elements)) >= 1,
                                'at_least_one_widget_constraint_%s' % device.name)
        else:
            # (12) a device which is not accessible by any user should not have a element
            model.addConstr(quicksum(x[e, d] for e, _ in enumerate(elements)) == 0,
                            'no_element_constraint_%s' % device.name)
    model.update()

    # Diversity variables and constraints
    user_num_unique_elements = {}
    user_num_element = {}
    user_num_replicated_elements = {}
    element_assigned_to_user = {}
    for u, user in enumerate(users):
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
        # NOTE: weighted by inverse element-user importance,
        #       that is, more important elements can be repeated
        user_num_replicated_elements[u] = model.addVar(vtype=GRB.CONTINUOUS)
        model.addConstr(user_num_replicated_elements[u]
                        == quicksum(float(1. - element_user_imp[e, u]) * (user_num_element[u, e] - element_assigned_to_user[e, u])
                                    for e, element in enumerate(elements)))

    model.update()

    # Variables to penalize assigning too many elements on a device
    # TODO: does not allow too small devices
    max_elements_per_device_guideline = 4
    device_num_elements = {}
    device_num_elements_sub_our_max = {}
    device_num_elements_over_max = {}
    for d, device in enumerate(devices):
        device_num_elements[d] = model.addVar(vtype=GRB.SEMIINT, lb=0, ub=len(elements))
        device_num_elements_sub_our_max[d] = model.addVar(vtype=GRB.INTEGER,
                                                          lb=-len(elements)-4, ub=len(elements))
        device_num_elements_over_max[d] = model.addVar(vtype=GRB.SEMIINT, lb=0, ub=len(elements))

        model.addConstr(device_num_elements[d]
                        == quicksum(x[e, d] for e, element in enumerate(elements)))
        model.addConstr(device_num_elements_sub_our_max[d] + max_elements_per_device_guideline
                        == device_num_elements[d])
        model.addGenConstrMax(device_num_elements_over_max[d],
                              [device_num_elements_sub_our_max[d], 0])

    model.update()

    # Objective function
    cost = 0

    alpha1 = 0.20
    alpha2 = 0.25
    beta   = 0.25
    gamma  = 0.15
    delta  = 0.15
    assert np.abs(alpha1 + alpha2 + beta + gamma + delta - 1.0) < 1e-6

    # Maximize importance in assignment
    cost += alpha1 * quicksum(
                element_device_imp[e, d] * x[e, d]
                for e, _ in enumerate(elements)
                    for d, device in enumerate(devices)
            ) / (len(elements) * len(devices))

    # Maximize compatibility in assignment
    cost += alpha2 * quicksum(
                element_device_comp[e, d] * x[e, d]
                for e, _ in enumerate(elements)
                    for d, device in enumerate(devices)
            ) / (len(elements) * len(devices))

    # Minimize (A_max - A) / A_max scaled by importance
    cost -= beta * quicksum(
                float(element_device_imp[e, d])
                * (min(element._max_area, device._area) - s[e, d]) / min(element._max_area, device._area)
                * x[e, d]
                for e, element in enumerate(elements)
                    for d, device in enumerate(devices)
            ) / (len(elements) * len(devices))

    # Penalty for assigning duplicate/replicate elements
    for u, user in enumerate(users):
        num_user_elements = np.sum(user_element_access[u, :])
        num_user_devices = np.sum(user_device_access[u, :])
        if num_user_elements > 0 and num_user_devices > 0:
            cost -= gamma * user_num_replicated_elements[u] \
                    / (num_user_elements * num_user_devices * len(users))

    # Penalty for assigning too much on one device
    cost -= delta * quicksum(device_num_elements_over_max[d]
                             for d, device in enumerate(devices)) / len(devices)

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
        if not hasattr(element, '_optimizer_size'):
            element._optimizer_size = {}
        element._optimizer_size[device.name] = s[e, d].x
        output[device].append(element)
    return output


def pre_process_objects(elements, devices, users):
    # compatibility_metric = 'distance'
    compatibility_metric = 'dot'

    num_elements = len(elements)
    num_devices = len(devices)
    num_users = len(users)

    # Normalize so values are in [0, 1]
    def normalized(vector):
        v_max = vector.max()
        v_min = 0.0  # vector.min()
        v_dif = v_max - v_min
        vector = vector - v_min
        if v_dif > 1e-6:
            vector = vector / v_dif
        return vector

    # Retrieve, store and normalize user-specific element importance
    element_user_imp = np.ones((num_elements, num_users))
    element_name_index = dict((element.name, i) for i, element in enumerate(elements))
    for u, user in enumerate(users):
        element_user_imp[:, u] = [element.importance for element in elements]
        for element_name, importance in user.importance.iteritems():
            element_user_imp[element_name_index[element_name], u] = importance

    # Calculate and create normalized matrix of element-device compatibility
    element_device_comp = np.zeros((num_elements, num_devices))
    for d, device in enumerate(devices):
        for e, element in enumerate(elements):
            element_device_comp[e, d] = device.calculate_compatibility(element, compatibility_metric)
        element_device_comp[:, d] = normalized(element_device_comp[:, d])

    # Set boolean matrix of user-device access
    # TODO: try continuous numbers
    user_device_access = np.zeros((num_users, num_devices))
    for d, device in enumerate(devices):
        for user in device.users:
            user_device_access[users.index(user), d] = 1

    # Set boolean matrix of user-element access
    user_element_access = np.zeros((num_users, num_elements))
    for e, element in enumerate(elements):
        for u, user in enumerate(users):
            # NOTE: we set access to False if importance 0
            if element.user_has_access(user) and element_user_imp[e, u] > 0.0:
                user_element_access[u, e] = 1
            else:
                element_user_imp[e, u] = 0

    for u, user in enumerate(users):
        element_user_imp[:, u] = normalized(element_user_imp[:, u])

    # Normalize element importances per device
    element_device_imp = np.asmatrix(element_user_imp) * np.asmatrix(user_device_access)
    for d, device in enumerate(devices):
        element_device_imp[:, d] = normalized(element_device_imp[:, d])

    # Add noise to prevent stalemates
    def add_noise(array):
        array += 1e-6 * np.random.random(size=array.shape)
    # add_noise(element_device_comp)
    # add_noise(element_device_imp)
    # add_noise(element_user_imp)

    return element_user_imp, element_device_imp, element_device_comp, user_device_access, \
           user_element_access
