Scenario Testing
================

## Running Scenarios
Simply run `python scenario_name.py` where `scenario_name` is replaced by `media_sharing` for example.

You will see the specified inputs and optimized outputs as well as any tests which have been specified.

## Writing Scenarios
See `media_sharing.py` for an example. You can specify elements, widget types, and devices using a text-based configuration.

A created scenario can then be *run*, where our optimizer attempts to assign widgets to devices. This is done by calling `Scenario::run()`.

## Test results
The output on success would be:

    TESTS
    =====

    Great! All expectations met.

An example output on failure is:

    TESTS
    =====

    1 FAILURE(S)
    (1) [FAIL] prev not assigned to Bob's Watch



## Writing Tests
A test can be specified when calling `Scenario::run()` using the keyword argument `expect={}`.

Here, you can specify a `device_name` to `list of element_names` mapping for elements you expect to find on certain devices.

The framework will check these expectations and report to you whether any could not be met.
