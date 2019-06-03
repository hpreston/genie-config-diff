#! /usr/bin/env python
"""Script that leverages Genie to make a random change to a DevNet Sandbox

This script will retrieve information from a device.

Copyright (c) 2018 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from genie.conf import Genie
from random import randrange, choice
from importlib import import_module

# Pick a random change file and import it
changenum = randrange(1,3)
change = import_module("change{}".format(changenum))

# Uncomment to print out the configuration change to be made.
# print("Change to be made: ", change.configuration_block)

print("Making a configuration change to some device in the testbed.")

# Initialize the testbed and pick a random device
testbed = Genie.init('sandbox-testbed.yaml')
device = choice(list(testbed.devices))

# Uncomment to print out the device being changed
# print("Device to be changed: {}".format(device))

# Connect to the chosen device
testbed.devices[device].connect(log_stdout=False)

# Send configuration change block
testbed.devices[device].configure(change.configuration_block)

# Disconnect 
testbed.devices[device].disconnect()

print("Done making change... now go try to find it with 'genie learn'!")
