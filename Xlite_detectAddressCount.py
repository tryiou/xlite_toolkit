#!/usr/bin/env python

# Script will try to detect past addressCount with remaining funds
# Start it with your desired batch of addresses to try per attempt
# EXAMPLE:
# python Xlite_detectAddressCount.py 25

# logic:
# gather 25 addresses on mnemo, check for funds,
# as long as funds are being found on those addresses, take another batch and retry
# stop as soon as nothing found on a batch
# edit the addressCount accordingly


import json
import os
import sys
from func_defs import rpc_call, get_settings_folder, run_bin, kill_bin


def set_address_count(coin, address_count, settings_folder):
    file = 'config-' + coin + '.json'
    file_path = os.path.join(settings_folder, file)
    with open(file_path) as f:
        data = json.load(f)
    data['addressCount'] = address_count
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print('set_address_count:', coin, address_count)


def search_for_funds(settings_folder, increment):
    final_result = {}
    with open('wallet_password.json') as f:
        wallet_password = json.load(f)
    files = os.listdir(settings_folder)
    for file in files:
        if file.endswith('.json') and file != 'config-master.json':
            file_path = os.path.join(settings_folder, file)
            with open(file_path) as f:
                data = json.load(f)
            file_without_extension = file.split('.')[0]  # Get the part before the first dot
            file_parts = file_without_extension.split('-')  # Split the name using hyphens
            coin = file_parts[-1]  # Get the last part of the name
            print(coin)
            address_count = data.get('addressCount')
            rpc_user = data.get('rpcUsername')
            rpc_password = data.get('rpcPassword')
            rpc_port = data.get('rpcPort')
            if rpc_port > 0:
                if address_count > 0:
                    counter = 0
                    # increment = 5
                    set_address_count(coin, increment, settings_folder)
                    current_address_count = increment
                    count = 0
                    done = False
                    while not done:
                        counter += 1
                        process = run_bin(wallet_password)  # Start a new process
                        getaddressesbyaccount = rpc_call('getaddressesbyaccount',
                                                         ['main'], 'http://127.0.0.1',
                                                         rpc_user,
                                                         rpc_password,
                                                         rpc_port)
                        # print('==>getaddressesbyaccount:', getaddressesbyaccount['result'], '\n')

                        if 'result' in getaddressesbyaccount:
                            print('counter:', counter, len(getaddressesbyaccount['result']),
                                  len(getaddressesbyaccount['result'][count:current_address_count]),
                                  count,
                                  current_address_count)
                            if len(getaddressesbyaccount['result'][count:current_address_count]) > 0:
                                getutxos = rpc_call('getutxos',
                                                    [coin,
                                                     getaddressesbyaccount['result'][count:current_address_count]],
                                                    'https://xliterevp.mywire.org',
                                                    '',
                                                    '',
                                                    '443')
                                print(getutxos)
                                print()
                                if not ('utxos' in getutxos):
                                    print('not ("utxos" in getutxos)')
                                    break
                                else:
                                    if len(getutxos['utxos']) == 0:
                                        if count == 0:
                                            count = 1
                                        set_address_count(coin, count, settings_folder)
                                        done = True
                                        final_result[coin] = count
                                    else:
                                        current_address_count += increment
                                        count += increment
                                        # kill_bin(process)
                                        set_address_count(coin, current_address_count, settings_folder)
                                kill_bin(process)  # Kill the process after the loop ends
                            else:
                                print('error?', getaddressesbyaccount)
                                kill_bin(process)
                                break
            print()
    # process.kill()
    print("Done!\n", final_result)


def main(increment):
    settings_folder = get_settings_folder()
    search_for_funds(settings_folder, increment)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        increment_arg = int(sys.argv[1])
    else:
        increment_arg = 20
    main(increment_arg)
