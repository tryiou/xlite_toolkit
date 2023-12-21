#!/usr/bin/env python

# Script will import private keys for a coin into a active xlite session.
# It require a running Xlite or Xlite-daemon session on same host.
#
# EXAMPLE:
# edit script with token and keys to import.
# python Xlite_privateKeysImport.py

token = "BLOCK"
private_keys = ["pk1", "pk2", "etc"]

import os
import json
import sys
import platform
import psutil

from func_defs import rpc_call, get_settings_folder, run_bin, kill_bin

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


def is_xlite_daemon_running():
    binary_name = 'xlite-daemon.exe' if platform.system() == 'Windows' else \
        'xlite-daemon-linux64' if platform.system() == 'Linux' else 'xlite-daemon-osx64'
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == binary_name:
            return True
    return False


if __name__ == '__main__':
    external_daemon = True
    if not is_xlite_daemon_running():
        external_daemon = False
        with open('wallet_password.json') as f:
            xlite_password = json.load(f)
        process = run_bin(xlite_password)
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
                if coin == token:
                    for pk in private_keys:
                        result = rpc_call('importprivkey',
                                          [pk],
                                          'http://127.0.0.1',
                                          rpc_user,
                                          rpc_password,
                                          rpc_port)
                        if result and "error" in result and result['error'] is None:
                            print(f"Token: {token} import pk: {pk} ok")
                        else:
                            print(f"Token: {token} import pk: {pk} error")

    if not external_daemon:
        kill_bin(process)
