# AdaM

Source code for the CHI 2018 paper:

> Park, Seonwook, Christoph Gebhardt, Roman Rädle, Anna Maria Feit, Hana Vrzakova, Niraj Ramesh Dayama, Hui-Shyong Yeo et al. "AdaM: Adapting Multi-User Interfaces for Collaborative Environments in Real-Time." In Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems, p. 184. ACM, 2018.

- Project page: https://ait.ethz.ch/projects/2018/adam/
- Video: https://youtu.be/we3THlGJ39Y

## Setup

Clone this repository with its submodules using a command such as:

    git clone --recursive git@github.com:swook/adam-dui.git


Install the [Gurobi Solver](http://www.gurobi.com/). The solver is [available for free](https://user.gurobi.com/download/licenses/free-academic) for academic purposes.

Install all necessary dependencies by running:

    sudo python2 setup.py install

To run the backend, execute:

    cd optimization
    python2 run_server.py


## Scenario Construction and Testing

To create and test scenarios, please read `README.md` in folder `scenarios/`.

<!--
## Frontend (Webstrates)

The frontend requires a manager instance that analyzes the target website, which will be distributed across devices. It also retains a list of connected devices. The manager calls the optimizer every time a device connects or disconnects and applies the optimized allocation and layout on all connected devices.

Manager: [https://hikaru.cs.au.dk/HJE9myS8b/stable/?copy](https://hikaru.cs.au.dk/HJE9myS8b/stable/?copy) (username: `web`, password: `strate`)

The simulator allows to simulate different device configurations. New devices can be added to the configuration using one of the four add buttons at the top of the simulator (`Add TV`, `Add Laptop`, `Add Tablet`, `Add Smartphone`, or `Add Smartwatch`). The `Clear Devices` button removes all devices from the current configuration. The red trash icon removes a particular device from the configuration.

Simulator: [https://hikaru.cs.au.dk/BJcEFi4UW/stable/?copy](https://hikaru.cs.au.dk/BJcEFi4UW/stable/?copy) (username: `web`, password: `strate`)

The target website is currently hard-coded and points to [https://hikaru.cs.au.dk/youtube/](https://hikaru.cs.au.dk/youtube/). To test it with real devices, open [https://hikaru.cs.au.dk/youtube/?deviceClass=tablet](https://hikaru.cs.au.dk/youtube/?deviceClass=tablet) and replace the value of `deviceClass` from `tablet` to either `tv`, `laptop`, `smartphone`, or `smartwatch`.
-->

## Demonstration Frontend (incl. Simulator)

To be made available soon.
