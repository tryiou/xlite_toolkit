import json
import requests
import time
import platform
import os
import subprocess
import sys


def rpc_call(method, params, url, rpc_user, rpc_password, rpc_port, display=False):
    max_retries = 4
    retry_delay = 5
    timeout = 5  # Default timeout in seconds

    url = url + ':' + str(rpc_port) + '/'
    payload = json.dumps({'method': method, 'params': params})
    headers = {"Content-Type": "application/json"}
    auth = (rpc_user, rpc_password)

    if display:
        print('rpc_call(', method, ',', params, ')', url)

    for retry in range(max_retries):
        try:
            response = requests.request('POST', url, data=payload, headers=headers, auth=auth, timeout=timeout)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            response_json = response.json()

            return response_json

        except requests.exceptions.HTTPError as e:
            print("HTTP Error:", e)

        except requests.exceptions.ConnectionError as e:
            print("Connection Error:", e)

        except Exception as e:
            print("Error:", e)

        if retry < max_retries - 1:
            print('Retrying in {} seconds...'.format(retry_delay))
            time.sleep(retry_delay)

    print('Max retries reached. Unable to complete the request.')
    return None


def get_settings_folder():
    system = platform.system()
    if system == 'Windows':
        return os.path.expandvars('%APPDATA%\\CloudChains\\settings')
    elif system == 'Darwin':  # MacOS
        return os.path.expanduser('~/Library/Application Support/CloudChains/settings')
    elif system == 'Linux':
        return os.path.expanduser('~/.config/CloudChains/settings')
    else:
        raise Exception('Unsupported operating system: ' + system)


def run_bin(xlite_pass):
    print('Starting xlite-daemon')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    system = platform.system()

    if system == 'Windows':
        binary_name = 'xlite-daemon.exe'
    else:
        binary_name = 'xlite-daemon'

    binary_path = os.path.join(script_dir, binary_name)

    if not os.path.exists(binary_path):
        print(f"Error: '{binary_name}' binary file not found.")
        sys.exit(1)

    arguments = []
    os.environ['WALLET_PASSWORD'] = xlite_pass['xlite_pass']
    # Execute the binary and detach it
    process = execute_binary(binary_path, arguments)
    time.sleep(1)
    return process


def execute_binary(binary_path, arguments):
    try:
        # Start the process and detach it
        process = subprocess.Popen([binary_path] + arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.DEVNULL, start_new_session=True)
        return process
    except Exception as e:
        # Handle any exceptions that occur during the execution
        print('Error:', e)
        return None


def kill_bin(process):
    print('Closing xlite-daemon')
    process.terminate()
    #    process.send_signal(subprocess.signal.SIGINT)
    process.wait()
