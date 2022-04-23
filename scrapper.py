import asyncio
import sys
import time

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
from telethon.tl.functions.channels import JoinChannelRequest, GetParticipantsRequest
from telethon.tl.types import InputPeerEmpty, ChannelParticipantsSearch
from python_socks import ProxyType
import config as config
import csv

file_member = sys.argv[1]

async def __main__():
    api_id = config.api_id
    api_hash = config.api_hash
    phone = '+84783807639'
    client = TelegramClient("session/%s/%s" % (phone,phone), api_id, api_hash,
                                    proxy=(ProxyType.SOCKS5, '209.127.138.185', 7282, True, 'akoujkvn', 'haejin8zcyag'))
    channel_username = sys.argv[1]
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        await client.sign_in(phone, input('40779'))
    await client(JoinChannelRequest(channel_username))
    chats = []
    last_date = None
    chunk_size = 200
    groups=[]

    result = await client(GetDialogsRequest(
                 offset_date=last_date,
                 offset_id=0,
                 offset_peer=InputPeerEmpty(),
                 limit=chunk_size,
                 hash = 0
             ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup== True:
                groups.append(chat)
        except:
            continue

    print('From Which Group Yow Want To Scrap A Members:')
    # i=0
    # for g in groups:
    #     print(str(i) + '- ' + g.title)
    #     i+=1
    #
    # g_index = input("Nhap 1 so: ")
    # target_group=groups[int(g_index)]

    print('Tim nap thanh vien ...')
    time.sleep(1)
    all_participants = []
    # all_participants = client.get_participants(target_group)
    my_filter = ChannelParticipantsSearch('')
    while_condition = True
    print('Fetching Members...')
    # all_participants = await client.get_participants(target_group)
    offset = 0

    while while_condition:

        participants = await client(
            GetParticipantsRequest(channel=channel_username, offset=offset, filter=my_filter, limit=200, hash=0))

        all_participants.extend(participants.users)
        offset += len(participants.users)

        if len(participants.users) < 1:
            while_condition = False

    all_participants.extend(participants.users)
    time.sleep(1)

    print('Dang luu ...')
    with open("{}.csv".format(file_member),"w",encoding='UTF-8') as f:#Enter your file name.
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
        for user in all_participants:
            if user.username is not None and len(user.username) > 0:
                if user.username:
                    username= user.username
                else:
                    username= ""
                if user.first_name:
                    first_name= user.first_name
                else:
                    first_name= ""
                if user.last_name:
                    last_name= user.last_name
                else:
                    last_name= ""
                name= (first_name + ' ' + last_name).strip()
                writer.writerow([username,user.id,user.access_hash,name])
    print('Members scraped successfully.......')
    print('Happy Hacking......')
loop = asyncio.new_event_loop()
loop.run_until_complete(__main__())
loop.close()