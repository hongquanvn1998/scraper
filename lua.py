import os, sys, random, asyncio, python_socks
from time import sleep
from telethon import TelegramClient, sync
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from telethon.tl.functions.messages import  GetHistoryRequest
from telethon.tl.functions.channels import JoinChannelRequest
import config as config
env = os.environ

while True:
    phone = input("Nhap So Dien Thoai:")
    if phone == 'xx':
        os.system('clear')
        break
    else:
        api_id = 2015084
        api_hash = '24e8f34925604e25a9b8d695b21cf333'
        client = TelegramClient("session/"+phone,api_id,api_hash,proxy=(python_socks.ProxyType.SOCKS5, '127.0.0.1', 4444))
        channel = ['coinpassion','BinanceVietnamese','vietnamtradecoin']
        client.connect()
        if not client.is_user_authorized():
            print(F"Session lỗi!" + phone)
            client.disconnect()
            continue
        else:
            for message in client.get_messages(777000, limit=1):
                msg = message.message
                you_code = msg.split()[2].rstrip('.')
                print ("Code =>> "+you_code)
                print(channel)
                for i in channel:
                    client(JoinChannelRequest(i))
                client.disconnect()
  