# flake8: noqa
if __name__ == '__main__' and __package__ is None:
    import sys
    sys.path.insert(0, '../optimization/')
from properties import Properties
from element import Element
from widget import Widget
from device import Device
from user import User

from common import *

scenario = Scenario()
scenario.add_users('alice', 'bob', 'caroline', 'darryl')

# Define all elements and widgets
scenario.add_elements_from_text(
    # Name | Importance | Size | Visual Quality | Properties
    #
    # Properties: visual_display, text_input,
    #             touch_pointing, mouse_pointing
    #
    # NOTE: Leave name and importance empty if additional widget type of same element
    '''
    video    | 10 | 10 | 3 | 5000
             |    |  5 | 2 | 5000
    play     |  9 |  1 | 1 | 1023
             |    |  3 | 2 | 1043
    next     |  2 |  1 | 1 | 1023
    prev     |  2 |  1 | 1 | 1023
    comments |  5 |  5 | 1 | 2511
    '''
)

# Define devices and users who can access devices
scenario.add_devices_from_text(
    # Name | Capacity | Properties | Users
    #
    # Properties: visual_display, text_input,
    #             touch_pointing, mouse_pointing
    '''
    TV               | 15 | 5000 | alice,bob,caroline,darryl
    Darryl's PC      |  8 | 4505 | caroline,darryl
    Tablet           |  4 | 3340 | alice,bob,caroline,darryl
    Caroline's Phone |  2 | 2230 | caroline
    Alice's Watch    |  1 | 1110 | alice
    Bob's Watch      |  1 | 1110 | bob
    Abandoned PC     |  5 | 3504 |
    '''
)

# User-specific importance values should be >= 0
scenario.adjust_user_importance('alice', 'play', 2)
scenario.adjust_user_importance('bob', 'next', 0)
scenario.adjust_user_importance('bob', 'prev', 0)

# These expectations will be checked when run() is called
scenario.expect({
    'Bob\'s Watch': ['play'],
    'Alice\'s Watch': ['play'],
})

scenario.run()
