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
list_phone = config.list_phone
channel = config.channel
send_to_channel = config.send_to_channel
num = 0

with open(r"question.csv", encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    # rows = list(rows)
    # message = rows[num][0]
    for row in rows:
        message = row[0]
        if num == len(list_phone):
            num = 0
        data = list_phone[num]
        phone = data['phone']
        ip = data['ip']
        port = data['port']
        message = ''
        client = TelegramClient("session/" + phone, api_id, api_hash)
                                # proxy=(python_socks.ProxyType.SOCKS5, ip, port))
        client.connect()
        if not client.is_user_authorized():
            print(F"Session lỗi!" + phone)
            client.disconnect()
            continue
        else:
            for i in channel:
                client(JoinChannelRequest(i))
            entity = client.get_entity(send_to_channel)
            client.send_message(entity=entity, message=str(message))
            print(F"Sent to %s with message %s !" % (send_to_channel, message))
            client.disconnect()
            num += 1
            sleep(300)
