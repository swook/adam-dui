# SoManyDevices

![SoManyDevices Demo](material/demo.gif)

## Backend (Optimizer)

Prerequisites:

 * Install Gurobi Optimization [http://www.gurobi.com/](http://www.gurobi.com/)

To install and run optimizer:

 * From the repository root:
    * Navigate to subfolder `simple-websocket-server`
    * Run `sudo python setup.py install`
    * Navigate to subfolder `optimization`
    * Run `python run_server.py`
    
## Fontend (Webstrates)

The frontend requires a manager instance that analyzes the target website, which will be distributed across devices. It also retains a list of connected devices. The manager calls the optimizer every time a device connects or disconnects and applies the optimized allocation and layout on all connected devices.

Manager: [https://hikaru.cs.au.dk/HJE9myS8b/stable/?copy](https://hikaru.cs.au.dk/HJE9myS8b/stable/?copy) (username: `web`, password: `strate`)

The simulator allows to simulate different device configurations. New devices can be added to the configuration using one of the four add buttons at the top of the simulator (`Add TV`, `Add Laptop`, `Add Tablet`, `Add Smartphone`, or `Add Smartwatch`). The `Clear Devices` button removes all devices from the current configuration. The red trash icon removes a particular device from the configuration.

Simulator: [https://hikaru.cs.au.dk/BJcEFi4UW/stable/?copy](https://hikaru.cs.au.dk/BJcEFi4UW/stable/?copy) (username: `web`, password: `strate`)

The target website is currently hard-coded and points to [https://hikaru.cs.au.dk/youtube/](https://hikaru.cs.au.dk/youtube/). To test it with real devices, open [https://hikaru.cs.au.dk/youtube/?deviceClass=tablet](https://hikaru.cs.au.dk/youtube/?deviceClass=tablet) and replace the value of `deviceClass` from `tablet` to either `tv`, `laptop`, `smartphone`, or `smartwatch`.
