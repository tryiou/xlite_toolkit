import platform
import os
import glob
import json
import requests

# configurable settings >>
only_funded_address = 1
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
    path = "/Users/" + username + "/Library/Application Support/CloudChains/settings"
else:
    print("no valid os detected, exiting")
    exit()


def instruct_wallet(method, params=[]):
    # print("instruct_wallet(", method, ",", params, ")")
    url = "http://127.0.0.1:" + str(rpc_port) + "/"
    payload = json.dumps({"method": method, "params": params})
    headers = requests.utils.default_headers()
    auth = (rpc_user, rpc_password)
    try:
        response = json.loads(requests.request("POST", url, data=payload, headers=headers, auth=auth).text)['result']
    except:
        print('No response from wallet, check xlite/cc is running on this machine')
        response = None
    return response


def list_pks():
    if rpc_port > 0:
        if only_funded_address == 0:
            get_addresses = instruct_wallet('getaddressesbyaccount', ["main"])
            if get_addresses:
                for address in get_addresses:
                    privkey = instruct_wallet('dumpprivkey', [address])
                    print(address, ":", privkey)
        else:
            list_unspent = instruct_wallet('listunspent', [])
            if list_unspent:
                last = ""
                for each in list_unspent:
                    if each['address'] != last:
                        print(each['address'], ":", instruct_wallet('dumpprivkey', [each['address']]))
                    last = each['address']


if __name__ == "__main__":
    print("formatage: \n\nCOIN\naddress : privatekey\n")
    for filename in glob.glob(os.path.join(path, '*.json')):
        if "config-master.json" not in filename:
            coin = filename[filename.find("-") + 1:-5]
            f = open(filename)
            config = json.load(f)
            f.close()
            if config["rpcEnabled"]:
                rpc_password = config["rpcPassword"]
                rpc_user = config["rpcUsername"]
                rpc_port = config["rpcPort"]
                print(coin)
                list_pks()
            print('')
