import converters
import optimize_device_assignment
import optimize_layout


def handle_web_input(web_input):
    elements, devices = converters.from_web(web_input)
    our_output = optimize(elements, devices)
    return converters.to_web(our_output)

'''

Input:
    elements (list of Element)

Output:
    dict (device_class => list of Element)
    {
        'tv': [Element1, Element2],
        'phone': [Element1, Element3],
        'watch': [Element1],
    }
'''
def optimize(elements, devices):
    # Run 1st optimization
    output = None
    while True:
        output = optimize_device_assignment.optimize(elements, devices)

        # If optimization failed, try increasing capacity of all devices by 1
        if output is None:
            for device in devices:
                device.capacity += 1
        else:
            # We have found a solution, break this infinite loop
            break

    # Run 2nd optimization
    for device_class, elements in output.items():
        output[device_class] = optimize_layout.optimize(elements)

    return output
