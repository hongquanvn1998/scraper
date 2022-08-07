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
send_to_channel = sys.argv[1]
file_message = sys.argv[2]
file_session = sys.argv[3]
file_phone = sys.argv[4]
timeout = sys.argv[5]

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

list_phone = []
with open('phone_messenge/%s' % file_phone) as f:
    lines = f.read().splitlines()
    for line in lines:
        list_phone.append(line)


async def __main__(_list_phone, _proxies):
    num = 0
    number_proxy = 0
    number_row = 0
    with open(r"question/%s" % file_message, encoding='UTF-8') as f:
        rows = list(csv.reader(f, delimiter=",", lineterminator="\n"))
        # for row in rows:
        while True:
            # row = rows[number_row]
            # message = row[0]
            message = rows[number_row][0]
            phone = _list_phone[num]
            get_proxy = _proxies[number_proxy]
            try:
                if file_session == 'fanpad':
                    client = TelegramClient("%s/%s" % (file_session, phone), api_id, api_hash,
                                            proxy=(python_socks.ProxyType.SOCKS5, get_proxy['ip'], get_proxy['port'], True,
                                                   get_proxy['user'], get_proxy['password']))
                else:
                    client = TelegramClient("%s/%s/%s" % (file_session, phone, phone), api_id, api_hash,
                                            proxy=(python_socks.ProxyType.SOCKS5, get_proxy['ip'], get_proxy['port'], True,
                                                   get_proxy['user'], get_proxy['password']))
                await client.connect()
                await client.start()
                if not await client.is_user_authorized():
                    print(F"Session lỗi!" + phone)
                    num = 0 if num == len(_list_phone) - 1 else num + 1
                    number_proxy = number_proxy + 1 if number_proxy < len(_proxies) - 1 else 0
                    number_row = number_row + 1 if number_row < len(rows) - 1 else 0
                    await client.disconnect()
                    continue
                else:
                    await client(JoinChannelRequest(send_to_channel))
                    entity = await client.get_entity(send_to_channel)
                    await client.send_message(entity=entity, message=str(message))
                    print(F"%s: Sent to %s with message %s !" % (phone, send_to_channel, message))
                    num = 0 if num == len(_list_phone) - 1 else num + 1
                    number_proxy = number_proxy + 1 if number_proxy < len(_proxies) - 1 else 0
                    number_row = number_row + 1 if number_row < len(rows) - 1 else 0
                    await client.disconnect()
                    sleep(float(timeout))
            except Exception as e:
                print('%s Something Error: %s' % (_list_phone[num], e))
                num = 0 if num == len(_list_phone) - 1 else num + 1
                number_proxy = number_proxy + 1 if number_proxy < len(_proxies) - 1 else 0
                number_row = number_row + 1 if number_row < len(rows) - 1 else 0

loop = asyncio.new_event_loop()
loop.run_until_complete(__main__(list_phone,proxies))
loop.close()