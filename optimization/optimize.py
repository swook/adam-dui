# Copyright 2018 AdaM Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
import converters
import optimize_device_assignment


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
    output, _ = optimize_device_assignment.optimize(elements, devices, users)
    return output
