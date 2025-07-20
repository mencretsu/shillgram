import asyncio
import os
import random
from telethon import TelegramClient
from datetime import datetime
from telethon.errors import ChatWriteForbiddenError, ChannelPrivateError, FloodWaitError

api_id = 1234 #your api id
api_hash = 'ur api hash'

session_folder = 'session'
session_name = 'autopost'
# numb input
phone_number = input("phone numb (ex: +62xxxx): ").strip()

with open('autopost.txt', 'r', encoding='utf-8') as f:
    text_to_post = f.read().strip()

with open('linkpost.txt', 'r', encoding='utf-8') as f:
    link_list = [line.strip() for line in f if line.strip()]

if not os.path.exists(session_folder):
    os.makedirs(session_folder)

async def main():
    client = TelegramClient(os.path.join(session_folder, session_name), api_id, api_hash)
    await client.start(phone=phone_number)
    await asyncio.sleep(random.uniform(18, 30))  # variasi delay aman

    log_lines = []
    async with client:
        for i, link in enumerate(link_list, start=1):
            try:
                await client.send_message(link, text_to_post)
                print(f"[{i}] ✅ Sent : {link}")
            except ChatWriteForbiddenError:
                print(f"[{i}] ❌ Not allowed kirim ke {link}")
            except ChannelPrivateError:
                print(f"[{i}] 🚫 Channel private / tidak bisa diakses: {link}")
            except FloodWaitError as e:
                print(f"[{i}] ⏱️ Kena spam delay, nunggu {e.seconds}s")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"[{i}] ⚠️ Error ngirim {link}: {e}")
            await asyncio.sleep(random.uniform(18, 30))  # Delay aman
        await asyncio.sleep(random.uniform(18, 30))  # Delay aman

    print("\n✅ All done")

if __name__ == '__main__':
    asyncio.run(main())
