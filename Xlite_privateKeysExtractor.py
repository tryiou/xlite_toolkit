#!/usr/bin/env python

# Script will print to console 'address' and associated 'dumpprivkey' of any addresses/coins
# It require a running Xlite or Xlite-daemon sesssion on same host
#
# launch parameter :
#       true to print only addresses with funds. (default if not argument provided)
#       false to print all the addresses from active session.
#
# EXAMPLE:
# python Xlite_privateKeysExtractor.py true


import os
import json
import sys
import platform
import psutil

from func_defs import rpc_call, get_settings_folder, run_bin, kill_bin, is_xlite_daemon_running

# Default value
only_funded_address = True
# Check command-line arguments
if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg.lower() in ['true', 't']:
        only_funded_address = True
    elif arg.lower() in ['false', 'f']:
        only_funded_address = False

path = get_settings_folder()


def list_pks():
    if rpc_port > 0:
        if only_funded_address:
            list_unspent = rpc_call('listunspent', [], 'http://127.0.0.1', rpc_user, rpc_password, rpc_port)
            #            list_unspent = instruct_wallet('listunspent', [])
            if 'result' in list_unspent:
                last = ''
                for each in list_unspent['result']:
                    if each['address'] != last:
                        pk = rpc_call('dumpprivkey', [each['address']], 'http://127.0.0.1', rpc_user, rpc_password,
                                      rpc_port)
                        if 'result' in pk:
                            print(each['address'], ':', pk['result'])
                    last = each['address']
        else:

            get_addresses = rpc_call('getaddressesbyaccount', ['main'], 'http://127.0.0.1', rpc_user, rpc_password,
                                     rpc_port)
            if 'result' in get_addresses:
                for address in get_addresses['result']:
                    privkey = rpc_call('dumpprivkey', [address], 'http://127.0.0.1', rpc_user, rpc_password, rpc_port)
                    if 'result' in privkey:
                        print(address, ':', privkey['result'])


if __name__ == '__main__':
    external_daemon = True
    if not is_xlite_daemon_running():
        external_daemon = False
        with open('wallet_password.json') as f:
            xlite_password = json.load(f)
        process = run_bin(xlite_password)
    print('only_funded_address:', only_funded_address)
    print('\nformat: \n\nCOIN\naddress : privatekey\n')
    files = os.listdir(path)
    for file in files:
        if file.endswith('.json') and file != 'config-master.json':
            file_path = os.path.join(path, file)
            # for filename in glob.glob(os.path.join(path, '*.json')):
            #    if 'config-master.json' not in filename and 'null' not in filename:
            file_without_extension = file.split('.')[0]  # Get the part before the first dot
            file_parts = file_without_extension.split('-')  # Split the name using hyphens
            coin = file_parts[-1]
            f = open(file_path)
            config = json.load(f)
            f.close()
            if config['rpcEnabled']:
                rpc_password = config['rpcPassword']
                rpc_user = config['rpcUsername']
                rpc_port = config['rpcPort']
                print(coin)
                try:
                    list_pks()
                except Exception as e:
                    print("Error:", e)
                    system = platform.system()
                    # anomaly with windows when running daemon as subprocess ?
                    if system == 'Windows' and not external_daemon:
                        kill_bin(process)
                        if not is_xlite_daemon_running():
                            process = run_bin(xlite_password)
            print('')
    if not external_daemon:
        kill_bin(process)
