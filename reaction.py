import config as config

from pyrogram import Client
from pyrogram.raw.functions.messages import GetMessageReactionsList

# api_id = config.api_id
# api_hash = config.api_hash
# app = Client(
#     "wingswap/+84823633697/+84823633697.session",
#     api_id=api_id,
#     api_hash=api_hash
# )

# chat_id = -123456789

# with app:
#     peer = app.resolve_peer(chat_id)
#     # await app.send_reaction(chat_id, message_id, "🔥")
#     for message in app.iter_history(chat_id=chat_id):
#         reactions = app.send(
#             GetMessageReactionsList(
#                 peer=peer,
#                 id=message.message_id,
#                 limit=100
#             )
#         )

import csv
import os, sys, random, asyncio, python_socks
from time import sleep
import config as config


import struct, base64
from telethon.sessions.string import StringSession
from telethon.sync import TelegramClient
from pyrogram.storage.storage import Storage
from pyrogram import utils

def telethon_to_unpack(string):
  ST = StringSession(string)
  return ST


def start_session(string):
  with TelegramClient(StringSession(string), 6 ,"eb06d4abfb49dc3eeb1aeb98ae0f581e") as ses:
    ml = ses.get_me()
  return ml


def pack_to_pyro(data, ses):
  Dt = Storage.SESSION_STRING_FORMAT if ses.id < utils.MAX_USER_ID_OLD else Storage.SESSION_STRING_FORMAT_64
  return base64.urlsafe_b64encode(
            struct.pack(
                Dt,
                data.dc_id,
                None,
                data.auth_key.key,
                ses.id,
                ses.bot
        )).decode().rstrip("=")


def tele_to_pyro(string):
    DL = telethon_to_unpack(string)
    MK = start_session(string)
    return pack_to_pyro(DL, MK)

env = os.environ
api_id = config.api_id
api_hash = config.api_hash
send_to_channel = sys.argv[1]
file_session = sys.argv[2]
file_phone = sys.argv[3]
message_id = sys.argv[4]

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
with open('phone_old/%s' % file_phone) as f:
    lines = f.read().splitlines()
    for line in lines:
        list_phone.append(line)


async def __main__(_list_phone, _proxies):
    num = 0
    number_proxy = 0
    for phone in _list_phone:
        # row = rows[number_row]
        # message = row[0]
        # phone = _list_phone[num]
        get_proxy = _proxies[number_proxy]
        try:
            if file_session == 'fanpad':
                client = Client(tele_to_pyro("%s/%s.session" % (file_session, phone)), api_id, api_hash,proxy=dict(scheme='socks5', hostname=get_proxy['ip'], port=int(get_proxy['port']), username=get_proxy['user'], password=get_proxy['password']))
            else:
                client = Client("%s/%s/%s.session" % (file_session, phone, phone), api_id, api_hash,
                                        proxy=(python_socks.ProxyType.SOCKS5, get_proxy['ip'], get_proxy['port'], True,
                                            get_proxy['user'], get_proxy['password']))
            async with client:
                chat_id = await client.get_chat(send_to_channel).linked_chat.id
                await client.join_chat(chat_id)
                await client.send_reaction(chat_id, 3, "🔥")
                number_proxy = number_proxy + 1 if number_proxy < len(_proxies) - 1 else 0
        except Exception as e:
            print('%s Something Error: %s' % (_list_phone[num], e))
            number_proxy = number_proxy + 1 if number_proxy < len(_proxies) - 1 else 0

loop = asyncio.new_event_loop()
loop.run_until_complete(__main__(list_phone,proxies))
loop.close()