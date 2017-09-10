# flake8: noqa
from common import *

# Name | Importance | min W | min H | max W | max H | Properties
# Properties: visual_display, text_input, touch_pointing, mouse_pointing
element_definitions = {
    'Presentation (View)':     '10 | 800 | 500 | 2000 | 2000 | 5000',
    'Presentation (Notes)':    '12 | 500 | 300 | 2000 | 2000 | 5011 | Presenter',
    'Presentation (Controls)': ' 8 | 300 | 100 | 1000 |  100 | 0053 | Presenter',
    'Notes (Shared)':          ' 6 | 300 | 500 | 1000 | 1500 | 0530',
    'Notes (Employee1)':       ' 4 | 300 | 500 | 1000 | 1500 | 0530 | Employee1',
    'Notes (Employee2)':       ' 4 | 300 | 500 | 1000 | 1500 | 0530 | Employee2',
    'Notes (Employee3)':       ' 4 | 300 | 500 | 1000 | 1500 | 0530 | Employee3',
    'Notes (Employee4)':       ' 4 | 300 | 500 | 1000 | 1500 | 0530 | Employee4',
    'Notes (Employee5)':       ' 4 | 300 | 500 | 1000 | 1500 | 0530 | Employee5',
    'Clock':                   ' 1 | 100 | 100 |  300 |  300 | 2000',
    'Quaterly Figures':        ' 4 | 300 | 400 |  800 | 1000 | 3000',
    'Search Engine':           ' 4 | 300 | 400 |  800 | 1500 | 1500',
    'Location List':           ' 4 | 300 | 400 |  800 | 1500 | 1500',
}
# Name | Width | Height | Properties | Users
# Properties: visual_display, text_input, touch_pointing, mouse_pointing
device_definitions = {
    'Projector1':         '1920 | 1080 | 5000 | Boss,Presenter,Employee1,Employee2,Employee3,Employee4,Employee5,Assistant',
    'Projector2':         '1920 | 1080 | 5000 | Boss,Presenter,Employee1,Employee2,Employee3,Employee4,Employee5,Assistant',

    'Phone (Boss)':       ' 375 |  667 | 0340 | Boss',
    'Tablet (Boss)':      '1440 | 1024 | 1250 | Boss',
    'Laptop (Boss)':      '1680 | 1028 | 3503 | Boss',

    'Phone (Presenter)':  ' 375 |  667 | 0340 | Presenter',
    'Laptop (Presenter)': '1680 | 1028 | 3503 | Presenter',
    'Watch (Presenter)':  ' 312 |  390 | 1020 | Presenter',

    'Phone (Employee1)':  '375 |  667 | 0340 | Employee1',
    'Phone (Employee2)':  '375 |  667 | 0340 | Employee2',
    'Phone (Employee3)':  '375 |  667 | 0340 | Employee3',
    'Phone (Employee4)':  '375 |  667 | 0340 | Employee4',

    'Laptop (Employee1)': '1680 | 1028 | 3503 | Employee1',
    'Laptop (Employee2)': '1680 | 1028 | 3503 | Employee2',
    'Laptop (Employee3)': '1680 | 1028 | 3503 | Employee3',
    'Laptop (Employee4)': '1680 | 1028 | 3503 | Employee4',

    'Watch (Employee5)':  ' 312 |  390 | 1020 | Employee5',
    'Laptop (Employee5)': '1680 | 1028 | 3503 | Employee5',
    'Tablet (Employee5)': '1440 | 1024 | 1250 | Employee5',

    'Laptop (Assistant)': '1680 | 1028 | 4503 | Assistant',
    'Tablet (Assistant)': '1440 | 1024 | 3250 | Assistant',
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
scenario.set_user_importance('Presenter', 'Clock', 6)
scenario.run(expect={
    'Projector1':         ['Presentation (View)', '~Notes (Shared)'],
    'Projector2':         ['Presentation (View)', '~Notes (Shared)'],
    'Laptop (Presenter)': ['Presentation (Notes)'],
    'Laptop (Assistant)': ['Notes (Shared)'],
    'Laptop (Boss)':      ['Notes (Shared)'],
    'Laptop (Employee1)': ['Notes (Employee1)'],
    'Laptop (Employee2)': ['Notes (Employee2)'],
    'Laptop (Employee3)': ['Notes (Employee3)'],
    'Laptop (Employee4)': ['Notes (Employee4)'],
    'Phone (Presenter)':  ['Presentation (Controls)'],
})



#########
# TEST 2: Adjust system to second state
###########
scenario = init('Task 2')
scenario.add_elements_from_text(pick(element_definitions,
    ['Presentation (View)',
     'Presentation (Notes)',
     'Presentation (Controls)',
     'Notes (Shared)',
     'Notes (Employee1)',
     'Notes (Employee2)',
     'Notes (Employee3)',
     'Notes (Employee4)',
     'Notes (Employee5)',
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
     'Phone (Employee1)',
     'Phone (Employee2)',
     'Phone (Employee3)',
     'Laptop (Employee1)',
     'Laptop (Employee2)',
     'Laptop (Employee3)',
     'Laptop (Employee4)',
     'Laptop (Employee5)',
     'Tablet (Employee5)',
     'Watch (Employee5)',
     'Tablet (Assistant)',
     'Laptop (Assistant)',
     ]))
scenario.set_user_importance('Boss', 'Notes (Shared)', 8)
scenario.set_user_importance('Assistant', 'Notes (Shared)', 8)
scenario.set_user_importance('Presenter', 'Clock', 6)
scenario.run(expect={
    'Projector1':         ['Presentation (View)', '~Notes (Shared)'],
    'Projector2':         ['Presentation (View)', '~Notes (Shared)'],
    'Laptop (Presenter)': ['Presentation (Notes)'],
    'Laptop (Assistant)': ['Notes (Shared)'],
    'Laptop (Boss)':      ['Notes (Shared)'],
    'Laptop (Employee1)': ['Notes (Employee1)'],
    'Laptop (Employee2)': ['Notes (Employee2)'],
    'Laptop (Employee3)': ['Notes (Employee3)'],
    # 'Laptop (Employee4)': ['Notes (Employee4)'],
    'Watch (Employee5)':  ['Clock'],
})


check_previous_tests_for_failure()
