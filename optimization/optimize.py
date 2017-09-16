import converters
import optimize_device_assignment
import optimize_layout


def handle_web_input(web_input):
    elements, devices, users, token = converters.json_to_our_inputs(web_input)
    users = [user for user in users if user.name != 'anonymous']  # TODO: remove this hack
    our_output = optimize(elements, devices, users)
    return converters.our_output_to_json(our_output, token=token)

'''

Input:
    elements (list of Element)

Output:
    dict (device_class => list of {element: Element, widget: Widget})
    {
        'tv': [{Element1, Widget}, {Element2, Widget}],
        'phone': [{Element1, Widget}, {Element3, Widget}],
        'watch': [{Element1, Widget}],
    }
'''
def optimize(elements, devices, users):
    # Run 1st optimization
    output, _ = optimize_device_assignment.optimize(elements, devices, users)

    # # Run 2nd optimization
    # for device_class, elements in output.items():
    #     output[device_class] = optimize_layout.optimize(elements)

    return output
