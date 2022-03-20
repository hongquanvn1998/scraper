import csv
import os, sys, random, asyncio, python_socks
from time import sleep
from telethon import TelegramClient, sync
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.channels import JoinChannelRequest
import config as config

env = os.environ
api_id = config.api_id
api_hash = config.api_hash
channel = config.channel
send_to_channel = sys.argv[1]
file_message = sys.argv[2]
file_session = sys.argv[3]
file_phone = sys.argv[4]
num = 0
number_proxy = 0

proxies = []
with open('proxies.txt') as f:
    lines = f.read().splitlines()
    for line in lines:
        proxy = {}
        arr = line.split(':')
        proxy['ip'] = arr[0]
        proxy['port'] = arr[1]
        proxy['user'] = arr[2]
        proxy['password'] = arr[3]
        proxies.append(proxy)

list_phone = []
with open('%s' % file_phone) as f:
    lines = f.read().splitlines()
    for line in lines:
        list_phone.append(line)

with open(r"%s" % file_message, encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    for row in rows:
        message = row[0]
        phone = list_phone[num]
        get_proxy = proxies[number_proxy]
        try:
            if file_session == 'fanpad':
                client = TelegramClient("%s/%s" % (file_session, phone), api_id, api_hash,
                                        proxy=(python_socks.ProxyType.SOCKS5, get_proxy['ip'], get_proxy['port'], True,
                                               get_proxy['user'], get_proxy['password']))
            else:
                client = TelegramClient("%s/%s/%s" % (file_session, phone, phone), api_id, api_hash,
                                        proxy=(python_socks.ProxyType.SOCKS5, get_proxy['ip'], get_proxy['port'], True,
                                               get_proxy['user'], get_proxy['password']))
            client.connect()
            if not client.is_user_authorized():
                print(F"Session lỗi!" + phone)
                num = 0 if num == len(list_phone) - 1 else num + 1
                number_proxy = number_proxy + 1 if number_proxy < len(proxies) - 1 else 0
                client.disconnect()
                continue
            else:
                client(JoinChannelRequest(send_to_channel))
                entity = client.get_entity(send_to_channel)
                client.send_message(entity=entity, message=str(message))
                print(F"%s: Sent to %s with message %s !" % (phone, send_to_channel, message))
                num = 0 if num == len(list_phone) - 1 else num + 1
                number_proxy = number_proxy + 1 if number_proxy < len(proxies) - 1 else 0
                client.disconnect()
                if send_to_channel == 'coinpassion':
                    sleep(1200)
                else:
                    sleep(600)
        except Exception as e:
            print('Something Error: ',e)
