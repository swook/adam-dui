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
from common import *

# Create scenario object
scenario = Scenario()

# Add users by name
users = ['Lecturer'] + ['User%03d' % i for i in range(999)]
scenario.add_users_by_names(*users)

# Define all elements and widgets
scenario.add_elements_from_text(
    # Name | Importance | min W | min H | max W | max H | Properties
    #
    # Properties: visual_display, text_input,
    #             touch_pointing, mouse_pointing
    #
    # NOTE: Leave name and importance empty if additional widget type of same element
    '''
    Time                   |  1 |  100 |  100 |  300 |  200 | 5000
    Slides                 |  0 | 1000 | 1000 | 2000 | 2000 | 5000
    Slide Notes            |  0 |  500 |  300 |  800 | 1000 | 4000
    '''
)

# Define devices and users who can access devices
scenario.add_devices_from_text(
    # Name | Width | Height | Properties | Users
    #
    # Properties: visual_display, text_input,
    #             touch_pointing, mouse_pointing
    '\n'.join(
        ['Whiteboard | 2000 | 1000 | 5050 | Lecturer'] +
        ['Laptop     | 1200 |  800 | 4504 | Lecturer'] +
        ['Device %03d | 2000 | 1000 | 5555 | User%03d' % (i, i) for i in range(999)]
    )
)

# User-specific importance values should be >= 0
# Default value is pre-defined element importance.
# See above for element importance definitions.
scenario.set_user_importance('Lecturer', 'Slides', 20)
scenario.set_user_importance('Lecturer', 'Slide Notes', 10)

# Now run optimizer and tests.
# Specified expectations will be checked when run() is called.
# To test for non-assignment of elements, prepend element name
# with ~, for example: ~comments
scenario.run()

