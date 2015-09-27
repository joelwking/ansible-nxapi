# ansible-nxapi
Ansible modules for managing Nexus switches using feature nxapi.

## nxapi_install_config

This module reads a configuration file and uses the nxapi feature to push the configuration using the nxapi interface. The module writes a log file to the /tmp directory and imbeds the julian date and userid running the module in the file name. There is a debug option which can be enabled to display the commands sent to the switch.  By using the debug option and commands which fail can be easily identified.

The design of the module is be a general purpose configuration tool, the user must create a valid series of commands for the switch. This is in contrast to other nx-api modules which implement a specific function using the arguments passed to the module. The use case for nxapi_install_config is to demonstrate the functionaly of the nx-api interface and to apply initial configurations to switches. On going operations might be better served from the modules found at 

[CiscoDevNet/nxos-ansible] (https://github.com/CiscoDevNet/nxos-ansible)

## csv_to_facts

Read the CSV file specified and output Ansible facts in the form of a list with each element in the list as a dictionary using the column header as the key and the contents of the cell as the value.

Typically this module would be followed by a task which runs the (Jinja) template module to apply the rows to a template. The subsequent step would then be to run a task using the module nxapi_install_config to then apply the config to the switch(s).

Network engineers frequently work from an Excel spreadsheet to specify information about ports on a switch, and this module is a simply means of gleaning that information and creating a configuration for each port. 

An example .CSV file might look like this:

```
SourceDeviceHostname,SourcePort,SourceIP,VLAN,Speed,DestinationDeviceHostname,DestinationPort,Note
13leafzn02-rp01,E1/10,none,10,1000,Spine-101,Ethernet1/10,"This is a note"
13leafzn02-rp01,E1/11,none,10,1000,Spine-101,Ethernet1/9,"Mary had a little lamb"
```

and the resulting output rendered from the template module would look like this:

```
interface E1/10
  speed 1000
  description peer: Spine-101: Ethernet1/10 This is a note
  switchport
  switchport access vlan 10
interface E1/11
  speed 1000
  description peer: Spine-101: Ethernet1/9 Mary had a little lamb
  switchport
  switchport access vlan 10
```
The template could contain global variable configurations in addition to looping through the rows of the CSV file. This provides a means to easily create baseline configurations when deploying new data center fabrics.


