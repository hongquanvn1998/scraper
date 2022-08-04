import sys

import python_socks
import config as config

try:
    from random import choice
    from requests import get
    from time import sleep
    from json import load, loads, dump, decoder
    from os import system, remove
    from sys import exit
    from telethon.sync import TelegramClient
    from telethon.errors import rpcerrorlist, SessionPasswordNeededError, PhoneNumberUnoccupiedError
    from configparser import ConfigParser, NoSectionError, NoOptionError
except Exception as e:
    input(f"Something wrong: {e}")

file_session = sys.argv[1]
file_phone = sys.argv[2]
api_id = config.api_id
api_hash = config.api_hash

list_phone = []
with open('phone_messenge/%s' % file_phone) as f:
    lines = f.read().splitlines()
    for line in lines:
        list_phone.append(line)

proxies = []
with open('proxies/%s.txt' % file_session) as f:
    lines = f.read().splitlines()
    for line in lines:
        proxy = {}
        arr = line.split(':')
        proxy['ip'] = arr[0]
        proxy['port'] = arr[1]
        proxy['user'] = arr[2]
        proxy['password'] = arr[3]
        proxies.append(proxy)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_ban():
    list = []
    number_proxy = 0
    with open('phone_messenge/%s' % file_phone) as f:
        d = f.read().splitlines()
    for i in d:
        print(f"day la i: {i}")
        get_proxy = proxies[number_proxy]
        client = TelegramClient(f"{file_session}/{i}.session", api_id, api_hash,
        proxy=(python_socks.ProxyType.SOCKS5, get_proxy['ip'], get_proxy['port'], True,
                                                   get_proxy['user'], get_proxy['password'])
        )
        client.connect()
        if not client.is_user_authorized():
            try:
                client.send_code_request(i)
            except rpcerrorlist.PhoneNumberBannedError:
                print(bcolors.FAIL+f"{i}: Banned"+bcolors.ENDC)
                client.disconnect()
                remove(f"{file_session}/{i}.session")
                number_proxy = number_proxy + 1 if number_proxy < len(proxies) - 1 else 0
        else:
            print(bcolors.OKGREEN+f"{i}: Active"+bcolors.ENDC)
            list.append(i)
            client.disconnect()
        number_proxy = number_proxy + 1 if number_proxy < len(proxies) - 1 else 0
    d = list
    print(f"Day la list {list}")
    with open('phone_messenge/%s' % file_phone, "w") as l:
        dump(d, l)
    input(bcolors.OKCYAN+"\nThe list is updated\n"+bcolors.ENDC)
    print("DONE")
    return

check_ban()