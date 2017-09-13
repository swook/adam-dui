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
    elements.sort(key=lambda x: x.name)
    devices.sort(key=lambda x: x.name)
    users.sort(key=lambda x: x.name)

    # Is there sufficient information to solve the assignment problem?
    if len(users) == 0 or len(devices) == 0 or len(elements) == 0:
        output = {}
        for device in devices:
            output[device] = []
        return output

    # Form input data
    element_user_imp, element_device_imp, element_device_comp, user_device_access, \
    user_element_access = pre_process_objects(elements, devices, users)

    # np.set_printoptions(precision=1)
    # print('element_user_imp:\n%s' % element_user_imp)
    # print('element_device_comp:\n%s' % element_device_comp)
    # print('element_device_imp:\n%s' % element_device_imp)
    # print('user_device_access:\n%s' % user_device_access)

    # Create empty model
    model = Model('device_assignment')
    # model.params.LogToConsole = 0  # Uncomment to see logs in console

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
        model.addConstr(quicksum(s[e, d] for e, _ in enumerate(elements)) <= device._area,
                        'capacity_constraint_%s' % device.name)

        for e, element in enumerate(elements):
            # (8,9) the min. width/height of an element should not exceed device width/height
            if element.min_width > device.width or element.min_height > device.height:
                model.addConstr(x[e, d] == 0,
                                'min_size_exceeds_constraint_%s_on_%s' % (element.name, device.name))

            # (10,11) Set s to zero if x is zero
            model.addGenConstrIndicator(x[e, d], False, s[e, d] == 0)
            model.addGenConstrIndicator(x[e, d], True, s[e, d] >= element._min_area)
            model.addGenConstrIndicator(x[e, d], True, s[e, d] <= min(element._max_area, device._area))

    model.update()

    # Make sure element privacy is respected.
    # All users must have access to a device as well as assigned elements.
    # That is, if there is even one user who is not authorised to view an element, the element
    # should not be assigned to the device.
    element_device_access = np.ones((len(elements), len(devices)), dtype=bool)
    for d, device in enumerate(devices):
        for e, element in enumerate(elements):
            # (13) user has no access to element so don't assign to user's device
            if np.any(user_device_access[:, d] > user_element_access[:, e]) or \
               not np.any(np.dot(user_device_access[:, d], user_element_access[:, e])):
                element_device_access[e, d] = 0

    model.update()

    for d, device in enumerate(devices):
        for e, element in enumerate(elements):
            # Do not assign inaccessible elements
            if element_device_access[e, d] == 0:
                model.addConstr(x[e, d] == 0,
                                name='privacy_%s_%s' % (element.name, device.name))

            # Do not assign 0-importance elements
            # TODO: add to paper
            elif element_device_imp[e, d] < 1e-5:
                element_device_access[e, d] = 0
                model.addConstr(x[e, d] == 0,
                                name='zero_importance_%s_%s' % (element.name, device.name))

            # Do not assign 0-compatibility elements
            # TODO: add to paper
            elif element_device_comp[e, d] < 1e-5:
                element_device_access[e, d] = 0
                model.addConstr(x[e, d] == 0,
                                name='zero_compatibility_%s_%s' % (element.name, device.name))
    model.update()

    for d, device in enumerate(devices):
        if np.any(element_device_access[:, d]):
            # (12) a device which is accessible by a user should have at least one element
            model.addConstr(quicksum(x[e, d] for e, _ in enumerate(elements)) >= 1,
                            'at_least_one_widget_constraint_%s' % device.name)
        else:
            # (12) a device which is not accessible by any user should not have a element
            model.addConstr(quicksum(x[e, d] for e, _ in enumerate(elements)) == 0,
                            'no_element_constraint_%s' % device.name)
    model.update()

    # Elements Diversity
    user_extra_elements = {}
    user_num_elements = {}
    user_num_elements_sub_1 = {}
    user_unique_elements = {}
    user_total_unique_elements = {}
    user_unassigned_elements = {}
    for u, user in enumerate(users):
        user_elements = [element for e, element in enumerate(elements) if user_element_access[u, e]]
        for e, element in enumerate(user_elements):
            user_num_elements[u, e] = model.addVar(vtype=GRB.SEMIINT)
            model.addConstr(user_num_elements[u, e] == quicksum(
                            user_element_access[u, e] * user_device_access[u, d] * x[e, d]
                            for d, _ in enumerate(devices)))

            user_num_elements_sub_1[u, e] = model.addVar(vtype=GRB.INTEGER, lb=-len(devices))
            model.addConstr(user_num_elements_sub_1[u, e] == user_num_elements[u, e] - 1)

            user_extra_elements[u, e] = model.addVar(vtype=GRB.INTEGER)
            model.addGenConstrMax(user_extra_elements[u, e], [user_num_elements_sub_1[u, e], 0])

            user_unique_elements[u, e] = model.addVar(vtype=GRB.BINARY)
            model.addGenConstrMax(user_unique_elements[u, e], [user_num_elements[u, e], 1])

        user_total_unique_elements[u] = model.addVar(vtype=GRB.SEMIINT)
        model.addConstr(user_total_unique_elements[u] == quicksum(
            user_unique_elements[u, e] for e, _ in enumerate(user_elements)
        ))

    # Objective function
    cost = 0

    compatibility_weight = 0.15
    quality_weight       = 0.4
    diversity_weight     = 0.45
    assert np.abs(compatibility_weight + quality_weight + diversity_weight - 1.0) < 1e-6

    for d, _ in enumerate(devices):
        num_elements = np.sum(element_device_access[: ,d])
        if num_elements > 0:
            # 1ST TERM: Maximize compatibility in assignment
            cost += compatibility_weight * quicksum(
                        element_device_comp[e, d] * x[e, d]
                        for e, _ in enumerate(elements)
                        if element_device_comp[e, d] > 0
                    ) / (num_elements * len(devices))

            # # 2ND TERM: Minimize (A_max - A) / A_max scaled by importance
            # max_area = min(element._max_area, device._area)
            # cost -= quality_weight * quicksum(
            #             float(element_device_imp[e, d])
            #             * (max_area - s[e, d]) / max_area
            #             for e, element in enumerate(elements)
            #             if element_device_imp[e, d] > 0
            #         ) / (num_elements * len(devices))

            # 2ND TERM: Maximize summed area of elements weighted by importance
            cost += quality_weight * quicksum(
                        element_device_imp[e, d] * s[e, d]
                        for e, element in enumerate(elements)
                        if element_device_imp[e, d] > 0
                    ) / (device._area * len(devices))

            # # 2ND TERM: Minimize difference to device capacity
            # cost -= quality_weight * (device._area - quicksum(
            #             element_device_imp[e, d] * s[e, d]
            #             for e, element in enumerate(elements)
            #             if element_device_imp[e, d] > 0
            #         )) / (device._area * len(devices))


    """
    # Term for assigning more less important elements for diversity
    num_user_devices = np.sum(user_device_access, axis=1)
    num_user_elements = np.sum(user_element_access, axis=1)
    for u, user in enumerate(users):
        if num_user_devices[u] > 0 and num_user_elements[u] > 0:
            cost += diversity_weight * quicksum(
                        # Inverse importance for less important elements
                        float((1.0 - element_user_imp[e, u]) * user_element_access[u, e]) *
                        quicksum(  # Number of elements user has access to
                            element_device_access[e, d] * x[e, d]
                            for d, _ in enumerate(devices)
                            if element_device_access[e, d]
                        )
                        for e, _ in enumerate(elements)
                        if user_element_access[u, e] and element_user_imp[e, u] < 1.0
                    ) / (num_user_elements[u] * num_user_devices[u] * len(users))
    """
    for u, user in enumerate(users):
        # user_devices = [device for d, device in enumerate(devices) if user_device_access[u, d]]
        user_elements = [element for e, element in enumerate(elements) if user_element_access[u, e]]
        if len(user_elements) == 0:
            continue
        cost += diversity_weight * user_total_unique_elements[u] / (len(user_elements) * len(users))

    model.setObjective(cost, GRB.MAXIMIZE)

    # Create output list of elements (sorted)
    output = {}
    for device in devices:
        output[device] = []

    # Solve
    model.optimize()
    if model.status != GRB.status.OPTIMAL:
        return output

    # for d, device in enumerate(devices):
    #     for e, element in enumerate(elements):
    #         print('%s [%d] - %s [%d] has size %d' % (device.name, d, element.name, e, s[e, d].x))

    # for e, element in enumerate(elements):
    #     for d, device in enumerate(devices):
    #         x_ = x[e,d].x
    #         s_ = s[e,d].x
    #         print('(%d,%d): x = %d, s = %d' % (e, d, x_, s_))

    # for u, user in enumerate(users):
    #     user_elements = [element for e, element in enumerate(elements) if user_element_access[u, e]]
    #     for e, _ in enumerate(user_elements):
    #         if user_element_access[u, e]:
    #             print('(%d,%d): max(%d - 1 = %d, 0) = %d' %
    #                   (e, d, user_num_elements[u, e].x, user_num_elements_sub_1[u, e].x,
    #                    user_extra_elements[u, e].x))

    for u, user in enumerate(users):
        print('%s has %d elements assigned:\n> %s' %
              (user.name, user_total_unique_elements[u].x,
               ', '.join(np.unique(sorted([element.name
                         for d, _ in enumerate(devices)
                         for e, element in enumerate(elements)
                         if x[e, d].x == 1 and user_device_access[u, d]])))))

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
    element_user_imp = np.zeros((num_elements, num_users))
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
    user_device_access = np.zeros((num_users, num_devices), dtype=bool)
    for d, device in enumerate(devices):
        for user in device.users:
            user_device_access[users.index(user), d] = 1

    # Set boolean matrix of user-element access
    user_element_access = np.zeros((num_users, num_elements), dtype=bool)
    for e, element in enumerate(elements):
        for u, user in enumerate(users):
            # NOTE: we set access to False if importance 0
            if element.user_has_access(user):
                user_element_access[u, e] = 1
            else:
                element_user_imp[e, u] = 0

    element_user_imp = np.multiply(element_user_imp, user_element_access.transpose())
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
