# ansible-nxapi

## csv_to_facts

Read a CSV file and output Ansible facts as a list of dictionaries. The column header is the key, the contents of each cell is the value.

Network engineers frequently work from an Excel spreadsheet to specify information about ports on a switch, and this module is a simply means of gleaning that information.

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
