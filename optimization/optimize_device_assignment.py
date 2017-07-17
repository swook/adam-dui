from gurobipy import *
import numpy as np

"""
Input:
    elements (list of Element)
    devices (list of Device)
    users (list of User)

Output:
    dict (device_class => list of {element: Element, widget: Widget})
    {
        'tv': [{Element1, Widget}, {Element2, Widget}],
        'phone': [{Element1, Widget}, {Element3, Widget}],
        'watch': [{Element1, Widget}],
    }
"""
def optimize(elements, devices, users):
    [widget_element_imp, element_user_imp, element_widget_device_comp, user_device_acc,
     widget_element_size, num_users, num_devices, num_elements, num_widgets] = pre_process_objects(elements, devices, users)

    # Create empty model
    model = Model('device_assignment')

    # Add decision variables
    x = {}
    for w in range(num_widgets):
        for e, element in enumerate(elements):
            for d, device in enumerate(devices):
                x[(w, e, d)] = model.addVar(vtype=GRB.BINARY, name='%i_%s_%s' % (w, element.name, device.name))
    model.update()

    for d, device in enumerate(devices):
        # Constraint 1: sum of widgets shouldn't exceed device class capacity
        model.addConstr(quicksum(widget_element_size[w, e] * x[(w, e, d)]
                                 for w in range(0, num_widgets)
                                    for e in range(0, num_elements)) <= device.capacity,
                            'capacity_constraint_%s' % device.name)

        if np.any(user_device_acc[:, d]):
            # Constraint 2: a device which is accessible by a user should have at least one widget
            model.addConstr(quicksum(x[(w, e, d)] for w in range(0, num_widgets)
                                                    for e in range(0, num_elements)) >= 1,
                            'at_least_one_widget_constraint_%s' % device.name)
        else:
            # Constraint 3: a device which is not accessible by any user should not have a widget
            model.addConstr(quicksum(x[(w, e, d)] for w in range(0, num_widgets)
                                                    for e in range(0, num_elements)) == 0,
                            'no_widget_constraint_%s' % device.name)

        for e, element in enumerate(elements):
            # Constraint 4: one device should not contain multiple representations of one UI element
            model.addConstr(quicksum(x[(w, e, d)] for w in range(0, num_widgets)) <= 1,
                            'one_element_widget_per_device_constraint_%s_%s' % (element.name, device.name))

        for e, element in enumerate(elements):
            for w in range(num_widgets):
                # Constraint 5: an assigned element should be of size > 0
                model.addConstr(widget_element_size[w, e] - x[(w, e, d)] >= 0,
                                'assigned_widget_size_nonzero_constraint_%d_%s' % (w, element.name))
    model.update()

    # Objective function
    cost = quicksum(widget_element_imp[w, e] * element_user_imp[e, u] * element_widget_device_comp[e, w, d] * user_device_acc[u, d] * x[(w, e, d)]
                    for w in range(num_widgets)
                        for e in range(num_elements)
                            for d in range(num_devices)
                                for u in range(num_users))
    model.setObjective(cost, GRB.MAXIMIZE)

    # Solve
    model.optimize()
    if model.status != GRB.status.OPTIMAL:
        return None

    # Create output list of elements (sorted)
    output = {}
    for device in devices:
        output[device] = []
    for key, var in x.items():
        if var.x != 1:  # Ignore if not 1.0 (assignment)
            continue
        w, e, d = key

        # Alert if for some reason widget of size <= 0 assigned
        assert widget_element_size[w, e] > 0

        element = elements[e]
        device = devices[d]
        widget = element.widgets[w]
        output[device].append({
            'element': element,
            'widget': widget,
        })
    return output


def pre_process_objects(elements, devices, users):
    num_elements = len(elements)
    num_devices = len(devices)
    num_users = len(users)
    num_widgets = 3
    # compatibility_metric = 'distance'
    compatibility_metric = 'dot'

    user_device_acc = np.zeros((num_users, num_devices))
    for d, device in enumerate(devices):
        for user in device.users:
            user_device_acc[users.index(user), d] = 1

    widget_element_imp = np.ones((num_widgets, num_elements)) * -1
    widget_element_size = np.zeros((num_widgets, num_elements))
    element_widget_device_comp = np.zeros((num_elements, num_widgets, num_devices))
    for e, element in enumerate(elements):
        for w, widget in enumerate(elements[e].widgets):
            widget_element_imp[w, e] = widget.visual_quality
            widget_element_size[w, e] = widget.size
            for d, device in enumerate(devices):
                element_widget_device_comp[e, w, d] = device.calculate_compatibility(widget, compatibility_metric)
                print(element)
                print(widget)
                print(device)
                print(element_widget_device_comp[e, w, d])
                print("")

    element_user_imp = np.zeros((num_elements, num_users))
    element_name_index = dict((element.name, i) for i, element in enumerate(elements))
    for u, user in enumerate(users):
        for element_name, importance in user.importance.iteritems():
            element_user_imp[element_name_index[element_name], u] = importance

    return [widget_element_imp, element_user_imp, element_widget_device_comp, user_device_acc,
     widget_element_size, num_users, num_devices, num_elements, num_widgets]
