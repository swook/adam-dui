# flake8: noqa
from common import *

# Create scenario object
scenario = Scenario()

# Add users by name
scenario.add_users_by_names('alice', 'bob', 'caroline', 'darryl')

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
             |    |  4 | 2 | 5000
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
    Tablet           |  5 | 3340 | alice,bob,caroline,darryl
    Caroline's Phone |  2 | 2230 | caroline
    Alice's Watch    |  1 | 1110 | alice
    Bob's Watch      |  1 | 1110 | bob
    Abandoned PC     |  5 | 3504 |
    '''
)

##########################################################
# 1. If Alice and Bob specifically put higher importance #
#    on the play element, it should be shown on their    #
#    watches.                                            #
##########################################################

# User-specific importance values should be >= 0
# Default is 1 for every user
scenario.set_user_importance('alice', 'play', 2)
scenario.set_user_importance('bob', 'play', 2)

# Now run optimizer and tests
# Specified expectations will be checked when run() is called
scenario.run(expect={
    'TV': ['video'],
    'Bob\'s Watch': ['play'],
    'Alice\'s Watch': ['play'],
})


##########################################################
# 2. When the TV is removed, the video should be         #
#    assigned to the Tablet and Darryl's PC.             #
##########################################################

# Remove all user-specific element importances
scenario.reset_all_user_importances()

# Remove TV
scenario.remove_device_by_name('TV')

# Now run optimizer and tests
scenario.run(expect={
    'Darryl\'s PC': ['video'],
    'Tablet': ['video'],
})
