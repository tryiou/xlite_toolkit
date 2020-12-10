import platform
import os
import glob
import json
import requests

# configurable settings >>
only_funded_address = 0
# configurable settings <<

username = os.getlogin()
# print(username)

system = platform.system()
# print(system)

if system == "Windows":
    path = "C:\\Users\\" + username + "\\AppData\\Roaming\\CloudChains\\settings"
elif system == "Linux":
    path = "/home/" + username + "/.config/CloudChains/settings/"
elif system == "Darwin":
    path = "/" + username + "/library/application support/CloudChains/settings/"
else:
    print("no valid os detected, exiting")
    exit()


def instruct_wallet(method, params):
    url = "http://127.0.0.1:" + str(rpc_port) + "/"
    payload = json.dumps({"method": method, "params": params})
    headers = {'content-type': "application/json", 'cache-control': "no-cache"}
    try:
        response = requests.request("POST", url, data=payload, headers=headers, auth=(rpc_user, rpc_password))
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        print(e)
    except:
        print('No response from Wallet, check xlite is running on this machine')


def rpc_call(command, parameter=[]):
    result = instruct_wallet(command, parameter)
    if result['error'] is not None:
        raise Exception(result['error'])
    else:
        return result['result']


def list_pks():
    if rpc_port > 0:
        if only_funded_address == 0:
            try:
                get_addresses = rpc_call('getaddressesbyaccount', ["main"])
            except Exception as e:
                print(e)
            else:
                for address in get_addresses:
                    privkey = rpc_call('dumpprivkey', [address])
                    print(address, ":", privkey)
        else:
            try:
                list_unspent = rpc_call('listunspent', [])
            except Exception as e:
                print(e)
            else:
                last = ""
                for each in list_unspent:
                    if each['address'] != last:
                        print(each['address'], ":", rpc_call('dumpprivkey', [each['address']]))
                    last = each['address']


print("formatage: \n\nCOIN\naddress : privatekey\n")
for filename in glob.glob(os.path.join(path, '*.json')):
    if "config-master.json" not in filename:
        print(filename[filename.find("-") + 1:-5])
        f = open(filename)
        config = json.load(f)
        f.close()
        if config["rpcEnabled"]:
            rpc_password = config["rpcPassword"]
            rpc_user = config["rpcUsername"]
            rpc_port = config["rpcPort"]
            list_pks()
        print('')
