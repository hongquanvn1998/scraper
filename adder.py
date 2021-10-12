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
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from itertools import islice
import config as config
import sys
import csv
import traceback
import time
import random

api_id = config.api_id
api_hash = config.api_hash
phone = '+84' + config.phone
client = TelegramClient(phone, api_id, api_hash)
async def main():
    # Now you can use all client methods listed below, like for example...
    await client.send_message('me', 'Hello !!!!!')


SLEEP_TIME_1 = 100
SLEEP_TIME_2 = 100
with client:
    client.loop.run_until_complete(main())
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('40779'))

users = []
with open(r"Scrapped.csv", encoding='UTF-8') as f:  #Enter your file name
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    # next(rows, None)
    for row in islice(rows, 2520, None):
    # for row in islice(rows, 350, None):
    # for row in rows[35:-1]:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
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

print('Chọn một nhóm để thêm thành viên: ')
i = 0
for group in groups:
    print(str(i) + '- ' + group.title)
    i += 1

g_index = input("Nhập một số ")
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

mode = int(input("Nhập 1 để thêm theo tên người dùng hoặc 2 để thêm theo ID: "))

n = 0
success = 0
failure = 0
privacy = 0
limit = 0

for user in users:
    n += 1
    print('Đã đến số: ',n)
    if n % 60 == 0:
        time.sleep(200)
    try:
        print("Adding {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Đã chọn chế độ không hợp lệ. Vui lòng thử lại.")
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        _sleep = random.randint(60, 200)
        success+=1
        print("Thành công lần thứ {}. Chờ {} giây ...".format(success,_sleep))
        print("=====================================================.")
        privacy = 0
        limit = 0
        time.sleep(_sleep)
    except PeerFloodError:
        limit+=1
        _sleep=0
        if limit < 3:
            _sleep = random.randint(100, 250)
        else:
            limit = 0
            _sleep = 600
        failure+=1
        print("Quá nhiều request. Vui lòng thử lại sau một thời gian.")
        print("Fail lần thứ {}. Thử lại sau {} seconds".format(failure,_sleep))
        print("=====================================================.")
        time.sleep(_sleep)
    except UserPrivacyRestrictedError:
        privacy+=1
        _sleep=0
        if privacy < 3:
            _sleep = random.randint(5, 20)
        else:
            privacy = 0
            _sleep = 200
        failure+=1
        print("Cài đặt quyền riêng tư của người dùng không cho phép bạn làm điều này. Bỏ qua.")
        print("Fail lần thứ {}. Chờ {} giây....".format(failure,_sleep))
        print("=====================================================.")
        time.sleep(_sleep)
    except:
        traceback.print_exc()
        failure+=1
        print("Fail lần thứ {}. Lỗi không mong đợi".format(failure))
        print("=====================================================.")
        continue
