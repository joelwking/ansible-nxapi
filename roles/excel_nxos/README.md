excel_nxos
=========

This role builds a Cisco NX-OS configuration from an Excel spreadsheet saved in CSV format.

Requirements
------------

Role Variables
--------------

The variables are derived from a CSV file, each line in the fie representing an interface on the
Nexus switch. The column headers are the varible names. These variable names are then referenced
in a template to render the configuration file to be loaded via the NX-API on the Nexus switch.

$ cat 13leafzn02-rp01.csv
SourceDeviceHostname,SourcePort,SourceIP,VLAN,Speed,DestinationDeviceHostname,DestinationPort,Note
13leafzn02-rp01,E1/10,none,10,1000,Spine-101,Ethernet1/10,"This is a note"
13leafzn02-rp01,E1/11,none,10,1000,Spine-101,Ethernet1/9,"Mary had a little lamb"
13leafzn02-rp01,E1/12,none,10,1000,Spine-101,Ethernet1/18,"The quick brown fox"
13leafzn02-rp01,E1/13,none,30,1000,Spine-102,Ethernet1/14,"jumped over the lazy dog"
13leafzn02-rp01,E1/14,none,30,1000,Spine-102,Ethernet1/13,"my dog has fleas"

Dependencies
------------

None

Example Playbook
----------------

    In a role configuration, given a group and host entry

      [asante]
      NEX-3048-E.sandbox.wwtatc.local  ansible_connection=local ansible_ssh_user=foo hostname=13leafzn02-rp01

      $ cat asante.yml
      ---
      - name: Test  Role
        hosts: asante

        roles:
          - {role: excel_nxos, debug: on}


      $ ansible-playbook asante.yml --ask-vault


License
-------

MIT

Author Information
------------------

joel.king@wwt.com 
