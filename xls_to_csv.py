#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     Copyright (c) 2019 World Wide Technology, Inc.
#     All rights reserved.
#
#     author: joel.king@wwt.com
#     written:  18 April 2019
#     linter: flake8
#         [flake8]
#         max-line-length = 160
#         ignore = E402
#
ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': '@joelwking'
}

DOCUMENTATION = '''
---
module: xls_to_csv.py
author: Joel w, King, World Wide Technology 
version_added: "2.9"
short_description: Read an Excel .xlsx file and output csv files for the specified sheets
description:
    - Read the XLS file specified and output a CSV file for each sheet specified
 
requirements:
    - The pandas library ust be installed on the Ansible host. This can be installed using pip:
    -   sudo pip install pandas
    -   sudo pip install xlrd

options:
    src:
        description:
            - The name of the Excel spreadsheet
        required: true

    dest: 
        description:
            - The destination directory to write the resulting CSV file
        required: true

    sheets:
        description:
            - The name(s) of the sheets to retrieve
        required: true 
'''

EXAMPLES = '''

     ansible localhost -m xls_to_csv -a 'dest=/tmp src=/it-automation-aci/TEST_DATA/WWT_ACI_Constructs_and_Policies.xlsx'

import xls_to_csv as xl
status, result = xl.read_xls('/it-automation-aci/TEST_DATA/WWT_ACI_Constructs_and_Policies.xlsx', 'Tenant-EPG')
xl.write_csv(result,'/tmp/')

'''

#
# Constants
#
ERROR = 0
OK = 1
EXTENSION = '.csv'

import os
import csv
import re

from ansible.module_utils.basic import AnsibleModule

try:
    MISSING_LIB = False
    import pandas as pd
    import xlrd                                            # pandas Install xlrd >= 0.9.0 for Excel support
except ImportError:
    MISSING_LIB = True    


def read_xls(input_file, sheets):
    """
    Read the .xlsx file and load everything into a dictionary of facts
    """
    result = {"ansible_facts": dict(),
              "warnings": []}
    data_frame = dict()                                    # each sheet in the file stored as data frame
    
    try:
        xlsx = pd.ExcelFile(input_file)
    except IOError:
        return (ERROR, "IOError on input file:%s" % input_file)

    
    for sheet in xlsx.sheet_names:                         # list of sheet names
        if sheet in sheets:
            data_frame[sheet] = xlsx.parse(sheet)              # read a specific sheet to DataFrame 
            result["ansible_facts"][get_valid_name(sheet)] = get_rows(data_frame[sheet])
        else:
            result['warnings'].append(' skipping sheet {} in source file'.format(sheet))
    
    return (OK, result)


def get_valid_name(name):
    """
        per Ansible https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html
        Variable names should be letters, numbers, and underscores. 
        Variables should always start with a letter.

        Remove special characters, spaces, leave underscores

    """
    name = re.sub(r"[^a-zA-Z0-9_]","", name)

    if name[0].isalpha():
        return name
    
    return 'Z_{}'.format(name)


def get_rows(data_frame):
    """
    data_frame: a data frame
    return: a list of dictionaries, the key is the column header and the value is the contents of the column

    Note: The column headers `for column in _df['Tenant-EPG'].columns:`
    """
    rows = []

    for row_number, row_content in data_frame.iterrows():         # returns a tuple row number and content
        row = {}
        for item in range(0, len(row_content)):
            column_name = get_valid_name(data_frame.columns[item])
            row[column_name] = row_content[item]
            # row[data_frame.columns[item]] = row_content[item]
        rows.append(row)
    
    return rows                                            # rows is a list of dictionaries

def write_csv(result, destination_dir):
    """
        Write the requested sheets to the destination directory
    """
    if not destination_dir:
        return (ERROR, "No output directory specified, nothing to write")

    if not destination_dir.endswith('/'):
        destination_dir + '/'

    for sheet in result['ansible_facts'].keys():
        try:
            output_file = destination_dir + sheet + EXTENSION
            f = open(output_file, 'w')
        except IOError:
            return (ERROR, "IOError on output file:%s" % output_file)

        fieldnames = result['ansible_facts'][sheet][0].keys() # TODO MERGE WITH BELOW
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in result['ansible_facts'][sheet]:
            try:
                writer.writerow(row)
            except UnicodeEncodeError:
                return(ERROR, '{} UnicodeEncodeError: {}'.format(sheet, row))
            
        f.close()

    result['ansbile_facts'] = {'sheet_filenames': result['ansible_facts'].keys()}

    return (OK, result)


def main():
    """
        Validate args, check for non-standard libraries, call functions to read XLS and write CSV
    """
    module = AnsibleModule(argument_spec = dict(
                 src = dict(required=True),
                 dest = dict(required=True),
                 sheets=dict(required=True, type='list')
             ),
             add_file_common_args=True)

    # we use the filename plus the sheet name
    # filename, extension = os.path.splitext(os.path.basename(input_file))

    if MISSING_LIB:
        module.fail_json(msg="The pandas and xlrd Python modules are required, install using: sudo pip install ...")

    status, result = read_xls(module.params["src"], module.params["sheets"])

    if status == ERROR:
        module.fail_json(msg=result)
    else:                                                  # Write sheets to destination directory
        status, result = write_csv(result, module.params.get("dest"))
        if status == ERROR:
            module.fail_json(msg=result)

        module.exit_json(**result)

    return code

if __name__ == '__main__':
    """ Run the program
    """
    main()
