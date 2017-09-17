#!/usr/bin/env python2
# flake8: noqa
import random
import string
import time

import matplotlib.pyplot as plt
import numpy as np

from user import User
from device import Device
from element import Element
from properties import Properties
from optimize_device_assignment import optimize

num_trials = 10

def vary_elements():
    n = 100
    devices = generate_devices(20)
    users = generate_users(10)
    assign_all_users_to_devices(users, devices)

    x = np.linspace(0, 5*n, num=n+1, dtype=np.int64)
    x[0] = 1
    y = [0] * n

    for i in range(n):
        time_diffs = []
        j = 0
        while j < num_trials:
            elements = generate_elements(x[i])

            time_diff, success = timed_optimize(elements, devices, users)
            if not success:
                print('%d failed' % x[i])
                continue
            time_diffs.append(time_diff)
            j += 1
        y[i] = np.mean(time_diffs)
        print('%d elements: %.2fs' % (x[i], y[i]))
    np.savetxt('vary_elements.txt', np.stack([x, y], axis=1))

def vary_devices():
    n = 100
    elements = generate_elements(20)
    users = generate_users(10, elements=elements)

    x = np.linspace(0, 5*n, num=n+1, dtype=np.int64)
    x[0] = 1
    y = [0] * n

    for i in range(n):
        time_diffs = []
        j = 0
        while j < num_trials:
            devices = generate_devices(x[i])
            assign_all_users_to_devices(users, devices)

            time_diff, success = timed_optimize(elements, devices, users)
            if not success:
                print('%d failed' % x[i])
                continue
            time_diffs.append(time_diff)
            j += 1
        y[i] = np.mean(time_diffs)
        print('%d devices: %.2fs' % (x[i], y[i]))
    np.savetxt('vary_devices.txt', np.stack([x, y], axis=1))

def vary_users():
    n = 20
    devices = generate_devices(50)
    elements = generate_elements(20)

    x = np.linspace(0, 500*n, num=n+1, dtype=np.int64)
    x[0] = 1
    y = [0] * n

    for i in range(n):
        time_diffs = []
        j = 0
        while j < num_trials:
            users = generate_users(x[i], elements=elements)
            assign_all_users_to_devices(users, devices)

            time_diff, success = timed_optimize(elements, devices, users)
            if not success:
                print('%d failed' % x[i])
                continue
            time_diffs.append(time_diff)
            j += 1
        y[i] = np.mean(time_diffs)
        print('%d users: %.2fs' % (x[i], y[i]))
    np.savetxt('vary_users.txt', np.stack([x, y], axis=1))

def vary_users_and_devices():
    n = 20
    elements = generate_elements(10)

    x = np.linspace(0, 100*n, num=n+1, dtype=np.int64)
    x[0] = 1
    y = [0] * n

    for i in range(n):
        time_diffs = []
        j = 0
        while j < num_trials:
            # 2 devices per user + 1 shared device per 5 users
            num_devices = 2 * x[i] + x[i] / 5
            devices = generate_devices(num_devices)
            users = generate_users(x[i], elements=elements)
            assign_all_users_to_devices(users, devices)
            for k in range(x[i]):
                devices[2*k].users = [users[k]]
                devices[2*k+1].users = [users[k]]

            time_diff, success = timed_optimize(elements, devices, users)
            if not success:
                print('%d failed' % x[i])
                continue
            time_diffs.append(time_diff)
            j += 1
        y[i] = np.mean(time_diffs)
        print('%d users & %d devices: %.2fs' % (x[i], num_devices, y[i]))
    np.savetxt('vary_users_and_devices.txt', np.stack([x, y], axis=1))

def generate_elements(n):
    rands_per_entry = 5
    all_rand_nums = np.random.random((rands_per_entry * n,))
    elements = []
    for i in range(n):
        a = rands_per_entry * i
        z = a + rands_per_entry
        rand_nums = all_rand_nums[a:z]
        elements.append(Element(
            name=random_name(),
            importance=int(10 * rand_nums[0]),
            min_width=int(10 + rand_nums[1] * 60),
            min_height=int(10 + rand_nums[2] * 60),
            max_width=int(80 + rand_nums[3] * 80),
            max_height=int(80 + rand_nums[4] * 80),
            requirements=random_properties(),
        ))
    return elements

def generate_devices(n):
    rands_per_entry = 2
    all_rand_nums = np.random.random((rands_per_entry * n,))
    devices = []
    for i in range(n):
        a = rands_per_entry * i
        z = a + rands_per_entry
        rand_nums = all_rand_nums[a:z]
        devices.append(Device(
            name=random_name(),
            width=int(20 + rand_nums[0] * 100),
            height=int(20 + rand_nums[1] * 100),
            affordances=random_properties(),
        ))
    return devices

def generate_users(n, elements=None):
    if elements is not None:
        rands_per_entry = len(elements)
        all_rand_nums = np.random.random((rands_per_entry * n,))
        element_names = [e.name for e in elements]
    users = []
    for i in range(n):
        if elements is not None:
            a = rands_per_entry * i
            z = a + rands_per_entry
            importance = dict(zip(element_names, all_rand_nums[a:z]))
            users.append(User(
                name=random_name(),
                id=random_name(),
                importance=importance,
            ))
        else:
            users.append(User(
                name=random_name(),
                id=random_name(),
            ))
    return users

def assign_all_users_to_devices(users, devices):
    for device in devices:
        device.users = users

def timed_optimize(elements, devices, users):
    start_time = time.time()
    output, time_taken = optimize(elements, devices, users)
    end_time = time.time()
    if np.any([len(v) for k, v in output.iteritems()]):
        print('total time taken: %.2fs' % (end_time - start_time))
        return time_taken, True
    else:
        return 0.0, False

chars = list(string.ascii_lowercase + string.digits)
def random_name():
    return ''.join(random.choice(chars) for _ in xrange(8))

def random_properties():
    return Properties(*np.random.random_integers(0, 5, (4, 1)))

def plot(func, xlabel, ylabel='Time to Solution / s'):
    log = np.loadtxt('%s.txt' % func.__name__)
    x = log[:, 0]
    y = log[:, 1]

    # Define figure
    fig = plt.figure(figsize=(3, 1.6))
    fig.subplots_adjust(bottom=0.12, left=0.16, top=0.99, right=0.97)

    # Plot data points
    plt.plot(x, y, 'r.-', aa=True)

    # Regression fit
    if func.__name__ == 'vary_users':
        p = np.polyfit(x, y, deg=1)
        plt.plot(x, p[0]*x**1 + p[1], 'g', label='linear fit', aa=True)
    else:
        p = np.polyfit(x, y, deg=2)
        plt.plot(x, p[0]*x**2 + p[1]*x**1 + p[2], 'b', label='quadratic fit', aa=True)

    # Labels
    plt.xlabel(xlabel)
    if func.__name__ == 'vary_elements':
        plt.ylabel(ylabel)
    plt.legend(frameon=False)

    # Axes adjustments
    ax = plt.gca()
    ax.yaxis.set_label_coords(-0.13, 0.43)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlim((0.0, ax.get_xlim()[1]))
    ax.set_ylim((0.0, ax.get_ylim()[1]))
    x_max = np.max(x)
    if x_max > 1000:
        plt.xticks(np.arange(0, x_max + 1, 2000))
    else:
        plt.xticks(np.arange(0, x_max + 1, 100))
    y_max = np.max(y)
    if y_max > 10.0:
        plt.yticks(np.arange(0, y_max + 0.1, 10))
    else:
        plt.yticks(np.arange(0, y_max + 0.1, 1))

    # Cosmetic changes
    # plt.grid(alpha=0.1, color='b')

    # Save
    plt.savefig('%s.pdf' % func.__name__)
    plt.clf()

if __name__ == '__main__':
    # vary_elements()
    # vary_devices()
    # vary_users()
    # vary_users_and_devices()
    plot(vary_elements, xlabel='Number of Elements')
    plot(vary_devices, xlabel='Number of Devices')
    plot(vary_users, xlabel='Number of Users')
    # plot(vary_users_and_devices, xlabel='Number of Users')
