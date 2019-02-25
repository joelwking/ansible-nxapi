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


class virt_spreadsheet(object):
    """
        Given a spreadsheet, we take each name and values entered as arguments, and
        create a virtual spreadsheet
    """
    def __init__(self, name, values, spreadsheet):
        self.name = name
        self.values = values
        self.spreadsheet = spreadsheet
        self.virt_set = set()
        self.virt_sheet = []
    def populate_sheet(self):
        for row in self.spreadsheet:
            virt_row = {}
            for column_header in self.values:
                virt_row[column_header] = row[column_header] 
            self.virt_set.add(tuple(virt_row.items()))            
        for item in self.virt_set:
            self.virt_sheet.append(dict(item))



def read_csv_dict(input_file, table_name, unique, vsheets):
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

    for ask in vsheets:
        obj = virt_spreadsheet(ask.get('name'), ask.get('values'), spreadsheet[table_name])
        obj.populate_sheet()
        spreadsheet[ask.get('name')] = obj.virt_sheet

    
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
                 unique=dict(default='spreadsheet_set', required=False, type='str'),
                 vsheets=dict(default=[], required=False, type='list')
                 ),
                 add_file_common_args=True)

    code, response = read_csv_dict(module.params["src"],
                                   module.params["table"],
                                   module.params["unique"],
                                   module.params['vsheets'])
    if code == 1:
        module.fail_json(msg=response)
    else:
        module.exit_json(**response)

    return code


main()
##############################################################################################################


def createlistoflist():
join = []
join.append([ 'Tenant', 'VRF'])
join.append(['Tenant', 'VRF', 'BD'])
join


# create the key (column header)
DELIMIT = ':'
for list in join:
    header = DELIMIT
    for item in list:
        header = header + item + DELIMIT
    header = header.strip(DELIMIT)
    return

    'Tenant:VRF:BD'


spreadsheet = [ {'Tenant':'WWT-INT', 'BD': 'WWT-BD1', 'VRF': 'WWT-VRF1'},
                {'Tenant':'WWT-EXT', 'BD': 'WWT-BD2', 'VRF': 'WWT-VRF1'},
                {'Tenant':'WWT-INT', 'BD': 'WWT-BD1', 'VRF': 'WWT-VRF1'}  ]

# create the value for a given key
def create_value(column_headers):

    value = {}
    

###
### main logic
###

### User enters a list of dictionaries
"""
  - name: BD_fields
    fields: 
      - Tenant
      - VRF
      - BD
  - name: VRF_fields
    fields:
      - Tenant
      - VRF
      
"""
joins = {}
joins['BD_fields'] = ['Tenant', 'VRF', 'BD']
joins['VRF_fields'] = ['Tenant', 'VRF']


class virt_spreadsheet(object):
    """
        Given a spreadsheet, we take each name and values entered as arguments, and
        create a virtual spreadsheet
    """
    def __init__(self, name, values, spreadsheet):
        self.name = name
        self.values = values
        self.spreadsheet = spreadsheet
        self.virt_sheet = []
    def populate_sheet(self):
        for row in self.spreadsheet:
            virt_row = {}
            for column_header in values:
                virt_row[column_header] = row[column_header] 
            self.virt_sheet.append(virt_row)            



    def create_set(rows, joins):
    """
        Return a dictionary with the column headers as keys, and the values are a
        list of unique values found in the rows of the spreadsheet for the column
        header (a set).

    """
    virtual_hdrs = {}                                   # create empty dictionary
    for key in rows[0].keys():                          # get column headers
        virtual_hdrs[key] = set()                        # create empty set for each header

    for row in rows:                                       # loop thru spreadsheet
        for key in row.keys():                             # for each column
            virtual_hdrs[key].add(row[key])              # populate the unique values

    return virtual_hdrs



#############################################
# Create a new row for the values of interest
#
def create_new_row(row, fields):
    """
      row: dictionary of the columns and values
      fields: list of the fields for the new row
    """ 
    new_row = {}
    for field in fields:
        new_row[field] = row[field]
    return tuple(new_row.items())












s = set()
for row in spreadsheet:
    s.add(tuple(row.items()))

# for each item in the set, create a row 
for item in s:
    row = dict(item)
    print row    