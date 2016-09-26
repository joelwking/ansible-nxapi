#!/usr/bin/env python

"""
     Copyright (c) 2015 World Wide Technology, Inc.
     All rights reserved.

     Revision history:
     26 Sept 2015  |  1.0 - initial release


"""

DOCUMENTATION = '''
---
module: csv_to_facts.py
author: Joel W. King, World Wide Technology
version_added: "1.01"
short_description: Read a CSV file and output Ansible facts
description:
    - Read the CSV file specified and output Ansible facts in the form of a list with each
      element in the list as a dictionary using the column header as the key and the contents
      of the cell as the value.

requirements:
    - None

options:
    src:
        description:
            - The CSV formatted input file
        required: true

    table:
        description:
            - The name of the list created
            - defaults to 'spreadsheet'
        required: false


'''

EXAMPLES = '''

    Running the module

      ansible  localhost  -m csv_to_facts -a "src=/tmp/TonyA.csv"
      ansible  localhost  -m csv_to_facts -a "src=/tmp/TonyA.csv table=my_data"

    In a role configuration, given a group and host entry

      [asante]
      NEX-3048-E.sandbox.wwtatc.local  ansible_connection=local ansible_ssh_user=kingjoe hostname=13leafzn02-rp01
      #

      $ cat asante.yml
      ---
      - name: Test  Role
        hosts: asante

        roles:
          - {role: excel_nxos, debug: on}


      $ ansible-playbook asante.yml --ask-vault

'''

import csv

# ---------------------------------------------------------------------------
# read_csv_dict
# ---------------------------------------------------------------------------

def read_csv_dict(input_file, table_name):
    "Read the CSV file and return as Ansible factsn"
    result = {"ansible_facts":{}}
    spreadsheet = {table_name:[]}

    try:
        with open(input_file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                 spreadsheet[table_name].append(row)
    except IOError:
        return (1, "IOError on input file:%s" % input_file)

    csvfile.close()

    result["ansible_facts"] = spreadsheet
    return (0, result)

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    " "
    module = AnsibleModule(argument_spec = dict(
             src = dict(required=True, type='str'),
             table = dict(default='spreadsheet', required=False, type='str')
             ),
             check_invalid_arguments=False,
             add_file_common_args=True)

    code, response = read_csv_dict(module.params["src"],
                                   module.params["table"])
    if code == 1:
        module.fail_json(msg=response)
    else:
        module.exit_json(**response)

    return code


from ansible.module_utils.basic import *
main()
#
