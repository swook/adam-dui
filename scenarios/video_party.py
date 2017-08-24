# flake8: noqa
from common import *

# Create scenario object
scenario = Scenario()

# Add users by name
scenario.add_users_by_names('alice', 'bob', 'caroline', 'darryl')

# Define all elements and widgets
scenario.add_elements_from_text(
    # Name | Importance | min W | min H | max W | max H | Properties
    #
    # Properties: visual_display, text_input,
    #             touch_pointing, mouse_pointing
    #
    # NOTE: Leave name and importance empty if additional widget type of same element
    '''
    video    | 10 | 500 | 300 | 2000 | 2000 | 5000
    play     |  9 | 100 | 100 |  500 |  500 | 1023
    next     |  2 | 100 | 100 |  500 |  500 | 1023
    prev     |  1 | 100 | 100 |  500 |  500 | 1023
    comments |  5 | 300 | 400 |  700 |  900 | 2511
    '''
)

# Define devices and users who can access devices
scenario.add_devices_from_text(
    # Name | Width | Height | Properties | Users
    #
    # Properties: visual_display, text_input,
    #             touch_pointing, mouse_pointing
    '''
    TV               | 1920 | 1600 | 5000 | alice,bob,caroline,darryl
    Darryl's PC      | 1920 | 1080 | 4505 | caroline,darryl
    Tablet           | 1280 |  720 | 3340 | alice,bob,caroline,darryl
    Caroline's Phone |  600 |  900 | 2230 | caroline
    Alice's Watch    |  150 |  150 | 1110 | alice
    Bob's Watch      |  150 |  150 | 1110 | bob
    Abandoned PC     | 1024 |  900 | 3504 |
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
    'Darryl\'s PC': ['comments'],
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
    'Darryl\'s PC': ['comments'],
    'Tablet': ['video'],
})
