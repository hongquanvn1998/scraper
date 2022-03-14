print ("")
print ("++++++---++++++++++++---++++++++++++---++++++++++++---++++++++++++---++++++")
print ("+  ____                                    ____ _           _    _         + ")
print ("- / ___|  __ _ _ __ ___   ___  ___ _ __   / ___| |__   ___ | | _| |_   _   -  ")
print ("+ \___ \ / _` | '_ ` _ \ / _ \/ _ \ '__| | |   | '_ \ / _ \| |/ / | | |    + ")
print ("-  ___) | (_| | | | | | |  __/  __/ |    | |___| | | | (_) |   <| | |_| |  -  ")
print ("+ |____/ \__,_|_| |_| |_|\___|\___|_|     \____|_| |_|\___/|_|\_\_|\__, |  +  ")
print ("-                                                                  |___/   -  ")
print ("++++++---++++++++++++---++++++++++++---++++++++++++---++++++++++++---++++++")
print ("")

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, InputUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, FloodWaitError
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from python_socks import ProxyType
import config as config
import sys
import csv
import traceback
import time
import random
import asyncio

api_id = config.api_id
api_hash = config.api_hash

users = []
with open(r"Scrapped.csv", encoding='UTF-8') as f:  #Enter your file name
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

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

# chats = []
# last_date = None
# chunk_size = 200
# groups = []
#
# result = client(GetDialogsRequest(
#     offset_date=last_date,
#     offset_id=0,
#     offset_peer=InputPeerEmpty(),
#     limit=chunk_size,
#     hash=0
# ))
# chats.extend(result.chats)
#
# for chat in chats:
#     try:
#         if chat.megagroup == True:
#             groups.append(chat)
#     except:
#         continue
#
# print('Chon nhom de them thanh vien: ')
# i = 0
# for group in groups:
#     print(str(i) + '- ' + group.title)
#     i += 1
#
# g_index = input("Nhap 1 so: ")
# target_group = groups[int(g_index)]
# target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

mode = 2

async def __main__():
    n = 0
    success = 0
    failure = 0
    privacy = 0
    limit = 0
    flood = 0
    number_phone = 0
    number_proxy = 0
    change_info = True
    target_group_entity = InputPeerChannel(1644207966, 4418609512849097208)
    for user in users:
        if change_info is True:
            phone = config.list_phone[number_phone]
            get_proxy = proxies[number_proxy]
            channel = config.channel[0]
            client = TelegramClient("session/%s/%s" % (phone, phone), api_id, api_hash,
                                    proxy=(ProxyType.SOCKS5, get_proxy['ip'], get_proxy['port'], True, get_proxy['user'], get_proxy['password']))

            await client.connect()
            is_authorized = await client.is_user_authorized()
            if not is_authorized:
                await client.send_code_request(phone)
                for message in client.get_messages(777000, limit=1):
                    msg = message.message
                    you_code = msg.split()[2].rstrip('.')
                await client.sign_in(phone, input(you_code))
            await client(JoinChannelRequest(channel))
            chats = []
            last_date = None
            chunk_size = 200
            groups = []

            result = await client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash=0
            ))
            chats.extend(result.chats)

            for chat in chats:
                try:
                    if chat.megagroup == True:
                        groups.append(chat)
                except:
                    continue

            for group in groups:
                if group.id == 1644207966:
                    target_group_entity = InputPeerChannel(group.id, group.access_hash)

        n += 1
        print('Da den so: %s\n User: %s \nPhone: %s'%(n, user['username'], phone))
        if n % 60 == 0:
            time.sleep(60)
        try:
            print("Adding {}".format(user['id']))
            # if mode == 1:
            #     if user['username'] == "":
            #         continue
            #     user_to_add = client.get_input_entity(user['username'])
            # elif mode == 2:
            # user_to_add = InputPeerUser(user['id'], user['access_hash'])
            user_to_add = await client.get_input_entity(user['username'])
            await client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            _sleep = random.randint(15, 20)
            success+=1
            print("Thanh cong {}. Cho {} seconds ...".format(success,_sleep))
            print("=====================================================.")
            change_info = False
            time.sleep(_sleep)
            await client.disconnect()
        except PeerFloodError:
            limit+=1
            if limit==10:
                number_phone = number_phone + 1 if number_phone < len(config.list_phone) else 0
                number_proxy = number_proxy + 1 if number_proxy < len(proxies) else 0
                change_info = True
                limit=0
            else:
                change_info = False
            _sleep = random.randint(60, 90)
            print("Qua nhieu request. Thu lai sau 1 thoi gian.")
            print("Limit lan thu {}. Thu lai sau {} seconds"
                  "\n flood={}"
                  "\n fail+private={} "
                  "\n success={}"
                  .format(limit, _sleep, flood, failure+privacy, success))
            print("=====================================================.")
            time.sleep(_sleep)
        except FloodWaitError:
            flood+=1
            if flood==5:
                number_phone = number_phone + 1 if number_phone < len(config.list_phone) else 0
                number_proxy = number_proxy + 1 if number_proxy < len(proxies) - 1 else 0
                change_info = True
                flood=0
            else:
                change_info = False
            _sleep = random.randint(25, 30)
            print("Flood lan thu {}. Thu lai sau {} seconds"
                  "\n limit={}"
                  "\n fail+private={} "
                  "\n success={}"
                  .format(flood, _sleep, limit, failure+privacy, success))
            print("=====================================================.")
            time.sleep(_sleep)
        except UserPrivacyRestrictedError:
            privacy += 1
            _sleep = random.randint(15, 20)
            change_info = False
            print("Cai dat quyen rieng tu khong cho phep them vao. Bo qua.")
            print("Privacy lan thu {}. Thu lai sau {} seconds. "
                  "\n limit={} "
                  "\n flood={}"
                  "\n fail+private={} "
                  "\n success={}"
                  .format(privacy, _sleep, limit, flood, failure+privacy, success))
            print("=====================================================.")
            time.sleep(_sleep)
        except:
            traceback.print_exc()
            failure += 1
            if failure == 200:
                number_phone = number_phone + 1 if number_phone < len(config.list_phone) else 0
                number_proxy = number_proxy + 1 if number_proxy < len(proxies) - 1 else 0
                change_info = True
                failure = 0
            else:
                change_info = False
            _sleep = random.randint(15, 20)
            change_info = False
            print("Fail lan thu {}. Loi khong mong doi. Thu lai sau {} seconds."
                  "\n limit={} "
                  "\n flood={}"
                  "\n fail+private={} "
                  "\n success={}"
                  .format(failure, _sleep, limit, flood, failure+privacy, success))
            print("=====================================================.")
            time.sleep(_sleep)
            continue
main_func = __main__()
# asyncio.run(__main__())
loop = asyncio.get_event_loop()
loop.run_until_complete(main_func)