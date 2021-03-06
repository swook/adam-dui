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

# Name | Importance | min W | min H | max W | max H | Properties
# Properties: visual_display, text_input, touch_pointing, mouse_pointing
element_definitions = {
    'Presentation (View)':     ' 7 | 1920 | 1080 | 2000 | 2000 | 5000',
    'Presentation (Notes)':    '10 |  500 |  500 | 2000 | 2000 | 4011 | Presenter',
    'Presentation (Controls)': ' 8 |  300 |  200 | 1000 |  200 | 0053 | Presenter',
    'Minutes (View)':          ' 5 |  375 |  667 |  800 | 1200 | 4000',
    'Minutes (Edit)':          ' 7 |  500 |  800 | 1000 | 1400 | 0505 | Boss,Assistant',
    'Notes (Employee)':        ' 3 |  800 |  500 | 1000 | 1500 | 0530 | Employee',
    'Clock':                   ' 1 |  150 |  150 |  300 |  300 | 1010',
    'Quaterly Figures':        ' 7 |  700 |  900 |  900 | 1500 | 5050 | Boss,Assistant',
}
# Name | Width | Height | Properties | Users
# Properties: visual_display, text_input, touch_pointing, mouse_pointing
device_definitions = {
    'Projector1':         '1920 | 1080 | 5000 | Boss,Presenter,Employee,Employee,Employee,Employee,Employee,Assistant',
    'Projector2':         '1920 | 1080 | 5000 | Boss,Presenter,Employee,Employee,Employee,Employee,Employee,Assistant',

    'Phone (Boss)':       ' 375 |  667 | 1340 | Boss',
    'Tablet (Boss)':      '1440 | 1024 | 3250 | Boss',
    'Laptop (Boss)':      '1680 | 1028 | 3503 | Boss',

    'Phone (Presenter)':  ' 375 |  667 | 1340 | Presenter',
    'Laptop (Presenter)': '1680 | 1028 | 3503 | Presenter',
    'Watch (Presenter)':  ' 312 |  390 | 1020 | Presenter',

    'Phone (Employee)':   ' 375 |  667 | 1340 | Employee',
    'Laptop (Employee)':  '1680 | 1028 | 3503 | Employee',
    'Tablet (Employee)':  '1440 | 1024 | 3250 | Employee',

    'Laptop (Assistant)': '1680 | 1028 | 4503 | Assistant',
    'Tablet (Assistant)': '1440 | 1024 | 3250 | Assistant',
}
def init(test_name):
    scenario = Scenario(test_name)
    return scenario
def pick(definitions, keys):
    return '\n'.join([key+'|'+definitions[key] for key in keys])

#########
# TEST 1: Initial expected configuration of users, devices and elements
###########
scenario = init('Task 1')
scenario.add_users_by_names('Boss', 'Presenter', 'Employee', 'Assistant')
scenario.add_elements_from_text(pick(element_definitions,
    ['Presentation (View)',
     'Presentation (Notes)',
     'Presentation (Controls)',
     'Minutes (View)',
     'Minutes (Edit)',
     'Notes (Employee)',
     'Clock',
     'Quaterly Figures',
     ]))
scenario.add_devices_from_text(pick(device_definitions,
    ['Projector1',
     'Projector2',

     'Phone (Boss)',
     'Tablet (Boss)',
     'Laptop (Boss)',

     'Phone (Presenter)',
     'Laptop (Presenter)',

     'Phone (Employee)',
     'Laptop (Employee)',

     'Laptop (Assistant)',
     ]))
scenario.set_user_importance('Assistant', 'Minutes (View)', 0)
scenario.set_user_importance('Boss', 'Minutes (View)', 0)
scenario.set_user_importance('Presenter', 'Clock', 6)
scenario.run(expect={
    'Projector1':         ['Presentation (View)'],
    'Projector2':         ['Presentation (View)'],
    'Laptop (Presenter)': ['Presentation (Notes)'],
    'Laptop (Assistant)': ['Minutes (Edit)', 'Quaterly Figures'],
    'Laptop (Boss)':      ['Minutes (Edit)'],
    'Tablet (Boss)':      ['Quaterly Figures'],
    'Laptop (Employee)':  ['Notes (Employee)'],
    'Phone (Presenter)':  ['Presentation (Controls)'],
})



#########
# TEST 2: Adjust system to second state
###########
scenario = init('Task 2')
scenario.add_users_by_names('Boss', 'Presenter', 'Employee', 'Assistant')
scenario.add_elements_from_text(pick(element_definitions,
    ['Presentation (View)',
     'Presentation (Notes)',
     'Presentation (Controls)',
     'Minutes (View)',
     'Minutes (Edit)',
     'Notes (Employee)',
     'Clock',
     'Quaterly Figures',
     ]))
scenario.add_devices_from_text(pick(device_definitions,
    ['Projector1',
     'Projector2',

     'Phone (Boss)',
     'Tablet (Boss)',
     'Laptop (Boss)',

     'Watch (Presenter)',
     'Phone (Presenter)',
     'Laptop (Presenter)',

     'Laptop (Employee)',
     'Tablet (Employee)',

     'Tablet (Assistant)',
     'Laptop (Assistant)',
     ]))
scenario.set_user_importance('Boss', 'Minutes (Edit)', 0)
scenario.set_user_importance('Boss', 'Minutes (View)', 7)
scenario.set_user_importance('Presenter', 'Clock', 6)
scenario.run(expect={
    'Projector1':         ['Presentation (View)'],
    'Projector2':         ['Presentation (View)'],
    'Laptop (Presenter)': ['Presentation (Notes)'],
    'Laptop (Assistant)': ['Minutes (Edit)'],
    'Tablet (Assistant)': ['Quaterly Figures'],
    'Laptop (Boss)':      ['~Minutes (Edit)'],
    'Tablet (Boss)':      ['Quaterly Figures'],
    'Laptop (Employee)':  ['Notes (Employee)'],
})

check_previous_tests_for_failure()

"""
#########
# TEST 3: Video Party
###########
scenario = init('Task 3')
scenario.add_users_by_names('Alice', 'Bob', 'Caroline', 'Darryl')
element_definitions = {
    'Video':             '10 | 1920 | 1080 | 2600 | 1600 | 5000',
    'Playback Controls': ' 9 |  150 |  100 |  300 |  300 | 0052 | Alice',
    'Suggestions':       ' 4 |  400 |  800 |  800 |  800 | 4043',
    'Comments':          ' 4 |  800 |  900 |  900 |  900 | 1500',
    'Voting Controls':   ' 6 |  150 |  100 |  300 |  200 | 0052',  # Yes or No
}

device_definitions = {
    'TV':                        '2600 | 1600 | 5000 | Alice,Bob,Caroline,Darryl',
    'Laptop':                    '1440 |  900 | 3503 | Alice,Bob,Caroline,Darryl',
    'Tablet (Caroline, Darryl)': '1280 | 1024 | 3250 | Caroline,Darryl',
    'Phone (Alice)':             ' 600 |  900 | 0330 | Alice',
    'Phone (Caroline)':          ' 600 |  900 | 0330 | Caroline',
    'Watch (Alice)':             ' 150 |  150 | 0020 | Alice',
    'Watch (Bob)':               ' 150 |  150 | 0020 | Bob',
    'Abandoned PC':              '1024 |  900 | 3505 |',
}
scenario.add_elements_from_text(pick(element_definitions,
    ['Video',
     'Playback Controls',
     'Suggestions',
     'Comments',
     'Voting Controls',
     ]))
scenario.add_devices_from_text(pick(device_definitions,
    ['TV',
     'Laptop',
     'Tablet (Caroline, Darryl)',
     'Phone (Alice)',
     'Phone (Caroline)',
     'Watch (Alice)',
     'Watch (Bob)',
     'Abandoned PC',
     ]))
scenario.set_user_importance('Darryl', 'Comments', 1)
scenario.set_user_importance('Darryl', 'Suggestions', 6)
scenario.run(expect={
    'TV':                        ['Video'],
    'Laptop':                    ['Comments'],
    'Tablet (Caroline, Darryl)': ['Suggestions', 'Voting Controls'],
    'Phone (Alice)':             ['Playback Controls'],
    'Phone (Caroline)':          ['Voting Controls'],
    'Watch (Alice)':             ['Voting Controls'],
    'Watch (Bob)':               ['Voting Controls'],
    'Abandoned PC':              [],
})

# END
check_previous_tests_for_failure()
"""
