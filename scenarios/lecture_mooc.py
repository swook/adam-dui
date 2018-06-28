# flake8: noqa
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

