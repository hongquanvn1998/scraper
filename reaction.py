# import config as config

# from pyrogram import Client
# from pyrogram.raw.functions.messages import GetMessageReactionsList

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

# import csv
# import os, sys, random, asyncio, python_socks
# from time import sleep
# from telethon import TelegramClient, sync
# from telethon.errors import SessionPasswordNeededError, FloodWaitError
# from telethon.tl.functions.messages import GetHistoryRequest
# from telethon.tl.functions.channels import JoinChannelRequest
# import config as config

# env = os.environ
# api_id = config.api_id
# api_hash = config.api_hash
# send_to_channel = sys.argv[1]
# file_session = sys.argv[2]
# file_phone = sys.argv[3]
# message_id = sys.argv[4]

# proxies = []
# with open('proxies/%s.txt' % file_session) as f:
#     lines = f.read().splitlines()
#     for line in lines:
#         proxy = {}
#         arr = line.split(':')
#         proxy['ip'] = arr[0]
#         proxy['port'] = arr[1]
#         proxy['user'] = arr[2]
#         proxy['password'] = arr[3]
#         proxies.append(proxy)

# list_phone = []
# with open('phone_messenge/%s' % file_phone) as f:
#     lines = f.read().splitlines()
#     for line in lines:
#         list_phone.append(line)


# async def __main__(_list_phone, _proxies):
#     num = 0
#     number_proxy = 0
#     number_row = 0
#     for phone in _list_phone:
#         # row = rows[number_row]
#         # message = row[0]
#         # phone = _list_phone[num]
#         get_proxy = _proxies[number_proxy]
#         try:
#             if file_session == 'fanpad':
#                 client = Client("%s/%s" % (file_session, phone), api_id, api_hash,
#                                         proxy=(python_socks.ProxyType.SOCKS5, get_proxy['ip'], get_proxy['port'], True,
#                                             get_proxy['user'], get_proxy['password']))
#             else:
#                 client = Client("%s/%s/%s" % (file_session, phone, phone), api_id, api_hash,
#                                         proxy=(python_socks.ProxyType.SOCKS5, get_proxy['ip'], get_proxy['port'], True,
#                                             get_proxy['user'], get_proxy['password']))
#             await client.connect()
#             await client.start()
#             if not await client.is_connected():
#                 print(F"Session lỗi!" + phone)
#                 await client.disconnect()
#                 continue
#             else:
#                 chat_id = await app.get_chat(send_to_channel).linked_chat.id
#                 await app.join_chat(chat_id)
#                 await client.send_reaction(chat_id, message_id, "🔥")
#             number_proxy = number_proxy + 1 if number_proxy < len(_proxies) - 1 else 0
#         except Exception as e:
#             print('%s Something Error: %s' % (_list_phone[num], e))
#             number_row = number_row + 1 if number_row < len(_proxies) - 1 else 0
#             number_proxy = number_proxy + 1 if number_proxy < len(rows) - 1 else 0

# loop = asyncio.new_event_loop()
# loop.run_until_complete(__main__(list_phone,proxies))
# loop.close()