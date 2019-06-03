# genie-config-diff
One of the most common questions network engineers have to figure out is "What configuration changed?".  [Genie](https://developer.cisco.com/pyats) from Cisco makes answering this question super easy.  And as a bonus, it can do far as well! 

In this repo will provide you a quick example walkthrough how you can use this tool in your own environment.  

## Prerequisites

* You can run this code against your own lab devices, but the code included is built leveraging the following DevNet Always On Sandboxes 
	* [IOS XE Always On Latest Code](https://devnetsandbox.cisco.com/RM/Diagram/Index/38ded1f0-16ce-43f2-8df5-43a40ebf752e?diagramType=Topology)
	* [NX-OS Always On Sandbox](https://devnetsandbox.cisco.com/RM/Diagram/Index/dae38dd8-e8ee-4d7c-a21c-6036bed7a804?diagramType=Topology) 
	* [IOS XR Always On Sandbox](https://devnetsandbox.cisco.com/RM/Diagram/Index/e83cfd31-ade3-4e15-91d6-3118b867a0dd?diagramType=Topology) 
* You'll need Python 3.4-3.7 installed and working. 
* You'll need a macOS or Linux environment to run the examples
	* *Windows users can leverage Window Subsystem for Linux* 

## Setting Up your Workstation 

1. Clone down the repo and change to the directory. 

	```bash
	git clone https://github.com/hpreston/genie-config-diff
	cd genie-config-diff
	```

1. Setup Python Virtual Env 

	```bash
	python3 -m venv venv 
	source venv/bin/activate
	pip install -r requirements.txt 
	```

1. If you're going to leverage the DevNet Sandboxes, the file [`sandbox-testbed.yaml`](sandbox-testbed.yaml) is ready to go, feel free to take a look at it.  
1. If you'd like to use your own lab gear you'll need to create a testbed file for your lab.  Check the [docs](https://pubhub.devnetcloud.com/media/pyats/docs/topology/creation.html#testbed-file) for how to create one, or just use [`sandbox-testbed.yaml`](sandbox-testbed.yaml) as a template.  

## Capturing the "Gold Config"
In order to find changes in the configuration, you need to capture a gold config.  One is included in the repository in the folder `sample_gold_config`, but you can also capture one of your own like this.  

1. Simply `learn config` using Genie CLI.  

	```bash
	genie learn config --testbed-file sandbox-testbed.yaml --output gold_config
	```
	
1. If you look in the `gold_config` folder, you'll find 3 files for each device in the topology.  
	* `connection_DEVICE.txt` - Raw console connection log for device 
	* `config_iosxe_DEVICE_console.txt` - Raw device output from the configuration capture 
	* `config_iosxe_DEVICE_ops.txt` - A JSON file created for the configuration 

## Making Some Network Change 
Now to change something that we want to find... you could wait around for something to change, but that could take a while.  Instead, go ahead and make a change.  

### Option 1: DIY with CLI
You can simply log into any of the sandbox devices we are working with using the connection info provide in the testbed or DevNet portal and use typical CLI commands to make some changes.  

### Option 2: Run one of the Provided Scripts 
In this repo I've provided a script that will make a configuration change on one or more of the devices for you.  I won't tell you what the changes are (but you could certainly look at the script) so you'll be surprised when you run the test.  

1. Simply run this script to make the change.  

	```bash
	python change_device_config.py
	```
	
## Finding the Change! 
Now for the good part, let's find the change.  

1. Re-learn the current configuration.  You need to provide a new value for the `output`.  

	```bash
	genie learn config --testbed-file sandbox-testbed.yaml --output changed
	```

1. Now find the `diff` between the `gold_config` and `changed`. 

	```bash
	genie diff gold_config changed
	
	# Output
	+==============================================================================+
	| Genie Diff Summary between directories gold_config/ and changed/             |
	+==============================================================================+
	|  File: config_iosxe_csr1000v-1_ops.txt                                       |
	|   - Diff can be found at ./diff_config_iosxe_csr1000v-1_ops.txt              |
	|------------------------------------------------------------------------------|
	|  File: config_iosxr_iosxr_ops.txt                                            |
	|   - Diff can be found at ./diff_config_iosxr_iosxr_ops.txt                   |
	|------------------------------------------------------------------------------|
	|  File: config_nxos_sbx-n9kv-ao_ops.txt                                       |
	|   - Diff can be found at ./diff_config_nxos_sbx-n9kv-ao_ops.txt              |
	|------------------------------------------------------------------------------|
	```

1. The output of the command shows you where the diffences are, and you can check the files referenced for the specific changes.  

	```diff
	--- gold_config/config_iosxe_csr1000v-1_ops.txt
	+++ changed/config_iosxe_csr1000v-1_ops.txt
	+Current configuration : 9351 bytes: 
	+interface Loopback1001: 
	+ description GenieLoop1001: 
	+ no ip address: 
	+interface Loopback1184: 
	+ description New Interface Created with Genie change: 
	+ no ip address: 
	-Current configuration : 9191 bytes: 
	```