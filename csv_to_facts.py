#!/usr/bin/env python
#
#     Copyright (c) 2019 World Wide Technology, Inc. All rights reserved.
#     GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': '@joelwking'
}

DOCUMENTATION = '''
---
module: csv_to_facts
short_description: Reads a CSV file and returns as ansible facts a list of dictionaries for each row

version_added: "2.8"

description:
    - Reads the CSV file specified and output Ansible facts in the form of a list with each
    - element in the list as a dictionary. The column header is used as the key and the contents
    - of the cell as the value. Also returns a dictionary with each column header as a key, the
    - value is a list of unique values for the column, a set.

options:
    src:
        description:
            - The CSV formatted input file
        required: true

    table:
        description:
            - The name of the list created, defaults to 'spreadsheet'
        required: false

    unique:
        description:
            - The variable name of containing a dictionary of unique values for each column
            - defaults to 'spreadsheet_set'
        required: false

author:
    - Joel W. King (@joelwking)
'''

EXAMPLES = '''

  - name: Read CSV and return as ansible_facts
    hosts: localhost
    vars:
      ifile: "./files/f5_wide_IP.csv"

    tasks:
    - name: Get facts from CSV file
      csv_to_facts:
        src: '{{ ifile }}'
        table: f5
        unique: f5_set
    - debug:
        msg: 'port: {{ item }}'
      loop: '{{ f5_set.port }}'

'''

import csv
from ansible.module_utils.basic import AnsibleModule


def read_csv_dict(input_file, table_name, unique):
    "Read the CSV file and return as Ansible facts"

    result = {"ansible_facts": {}}
    spreadsheet = {table_name: [],
                   unique: {}
                   }

    try:
        with open(input_file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                spreadsheet[table_name].append(row)
    except IOError:
        return (1, "IOError on input file:%s" % input_file)

    csvfile.close()

    spreadsheet[unique] = create_set(spreadsheet[table_name])

    result["ansible_facts"] = spreadsheet
    return (0, result)


def create_set(rows):
    """
        Return a dictionary with the column headers as keys, and the values are a
        list of unique values found in the rows of the spreadsheet for the column
        header (a set).

    """
    column_headers = {}                                    # create empty dictionary
    for key in rows[0].keys():                             # get column headers
        column_headers[key] = set()                        # create empty set for each header

    for row in rows:                                       # loop thru spreadsheet
        for key in row.keys():                             # for each column
            column_headers[key].add(row[key])              # populate the unique values

    return column_headers


def main():
    """
    MAIN
    """
    module = AnsibleModule(argument_spec=dict(
                 src=dict(required=True, type='str'),
                 table=dict(default='spreadsheet', required=False, type='str'),
                 unique=dict(default='spreadsheet_set', required=False, type='str')
                 ),
                 add_file_common_args=True)

    code, response = read_csv_dict(module.params["src"],
                                   module.params["table"],
                                   module.params["unique"])
    if code == 1:
        module.fail_json(msg=response)
    else:
        module.exit_json(**response)

    return code


main()
