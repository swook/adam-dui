# flake8: noqa
from common import *

# Name | Importance | min W | min H | max W | max H | Properties
# Properties: visual_display, text_input, touch_pointing, mouse_pointing
element_definitions = {
    'Presentation (View)':     '10 | 800 | 500 | 2000 | 2000 | 5000',
    'Presentation (Notes)':    '12 | 800 | 500 | 1000 |  700 | 4331 | Presenter',
    'Presentation (Controls)': '15 | 300 | 100 | 1000 |  100 | 0053 | Presenter',
    'Notes (Shared)':          ' 6 | 300 | 500 | 1000 | 1500 | 0530 | Boss,Employee1,Employee2,Employee3,Employee4,Employee5,Assistant',
    'Notes (Employee1)':       ' 8 | 300 | 500 | 1000 | 1500 | 0530 | Employee1',
    'Notes (Employee2)':       ' 8 | 300 | 500 | 1000 | 1500 | 0530 | Employee2',
    'Notes (Employee3)':       ' 8 | 300 | 500 | 1000 | 1500 | 0530 | Employee3',
    'Notes (Employee4)':       ' 8 | 300 | 500 | 1000 | 1500 | 0530 | Employee4',
    'Notes (Employee5)':       ' 8 | 300 | 500 | 1000 | 1500 | 0530 | Employee5',
    'Timer':                   ' 8 | 100 | 100 |  400 |  400 | 2040 | Presenter',
    'Quaterly Figures':        ' 4 | 300 | 400 |  800 | 1500 | 3032',
    'Search Engine':           ' 4 | 300 | 400 |  800 | 1500 | 1500',
    'Location List':           ' 4 | 300 | 400 |  800 | 1500 | 1500',
}
# Name | Width | Height | Properties | Users
# Properties: visual_display, text_input, touch_pointing, mouse_pointing
device_definitions = {
    'Projector1':         '1920 | 1080 | 5000 | Boss,Presenter,Employee1,Employee2,Employee3,Employee4,Employee5,Assistant',
    'Projector2':         '1920 | 1080 | 5000 | Boss,Presenter,Employee1,Employee2,Employee3,Employee4,Employee5,Assistant',

    'Phone (Boss)':       ' 375 |  667 | 0330 | Boss',
    'Tablet (Boss)':      '1440 | 1024 | 1250 | Boss',
    'Laptop (Boss)':      '1680 | 1028 | 3503 | Boss',

    'Phone (Presenter)':  ' 375 |  667 | 0330 | Presenter',
    'Laptop (Presenter)': '1680 | 1028 | 3503 | Presenter',
    'Watch  (Presenter)': ' 312 |  390 | 0020 | Presenter',

    'Phone (Employee1)':  '375 |  667 | 0330 | Employee1',
    'Phone (Employee2)':  '375 |  667 | 0330 | Employee2',
    'Phone (Employee3)':  '375 |  667 | 0330 | Employee3',
    'Phone (Employee4)':  '375 |  667 | 0330 | Employee4',

    'Laptop (Employee1)': '1680 | 1028 | 3503 | Employee1',
    'Laptop (Employee2)': '1680 | 1028 | 3503 | Employee2',
    'Laptop (Employee3)': '1680 | 1028 | 3503 | Employee3',
    'Laptop (Employee4)': '1680 | 1028 | 3503 | Employee4',

    'Watch (Employee5)':  ' 312 |  390 | 0020 | Employee5',
    'Laptop (Employee5)': '1680 | 1028 | 3503 | Employee5',
    'Tablet (Employee5)': '1440 | 1024 | 1250 | Employee5',

    'Laptop (Assistant)': '1680 | 1028 | 3503 | Assistant',
    'Tablet (Assistant)': '1440 | 1024 | 1250 | Assistant',
}
def init(test_name):
    scenario = Scenario(test_name)
    scenario.add_users_by_names('Boss', 'Presenter', 'Employee1', 'Employee2', 'Employee3',
                                'Employee4', 'Employee5', 'Assistant')
    return scenario
def pick(definitions, keys):
    return '\n'.join([key+'|'+definitions[key] for key in keys])

#########
# TEST 1: Initial expected configuration of users, devices and elements
###########
scenario = init('Task 1')
scenario.add_elements_from_text(pick(element_definitions,
    ['Presentation (View)',
     'Presentation (Notes)',
     'Presentation (Controls)',
     'Notes (Shared)',
     'Notes (Employee1)',
     'Notes (Employee2)',
     'Notes (Employee3)',
     'Notes (Employee4)',
     'Timer',
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
     'Phone (Employee1)',
     'Phone (Employee2)',
     'Phone (Employee3)',
     'Phone (Employee4)',
     'Laptop (Employee1)',
     'Laptop (Employee2)',
     'Laptop (Employee3)',
     'Laptop (Employee4)',
     'Laptop (Assistant)',
     ]))
scenario.set_user_importance('Boss', 'Notes (Shared)', 8)
scenario.set_user_importance('Assistant', 'Notes (Shared)', 8)
scenario.run(expect={
    'Projector1':         ['Presentation (View)'],
    'Projector2':         ['Presentation (View)'],
    'Laptop (Presenter)': ['Presentation (Notes)'],
    'Laptop (Assistant)': ['Notes (Shared)'],
    'Laptop (Boss)':      ['Notes (Shared)'],
    'Laptop (Employee1)': ['Notes (Employee1)'],
    'Laptop (Employee2)': ['Notes (Employee2)'],
    'Laptop (Employee3)': ['Notes (Employee3)'],
    'Laptop (Employee4)': ['Notes (Employee4)'],
    'Phone (Presenter)':  ['Timer'],
})

