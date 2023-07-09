#!/usr/bin/env python

# Script will change addressCount used by Xlite/xlite-daemon
# Start it with your desired addressCount
# EXAMPLE:
# python Xlite_changeAddressCount.py 20

import json
import os
import sys
from func_defs import get_settings_folder


def replace_address_count(settings_folder, address_count):
    files = os.listdir(settings_folder)
    for file in files:
        if file.endswith('.json') and file != 'config-master.json':
            file_path = os.path.join(settings_folder, file)
            with open(file_path) as f:
                data = json.load(f)
            ancient_address_count = data.get('addressCount')
            print(f'Filename: {file}')
            print(f'Ancient Address Count: {ancient_address_count}')
            data['addressCount'] = address_count
            print(f'New Address Count: {address_count}')
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)


def main(address_count):
    settings_folder = get_settings_folder()
    replace_address_count(settings_folder, address_count)


if __name__ == '__main__':
    addr_count = 20
    if len(sys.argv) > 1:
        addr_count = int(sys.argv[1])
    main(addr_count)
