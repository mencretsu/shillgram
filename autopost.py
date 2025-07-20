import asyncio
import os
import random
from telethon import TelegramClient
from datetime import datetime
from telethon.errors import ChatWriteForbiddenError, ChannelPrivateError, FloodWaitError

api_id = 28190254
api_hash = 'd0dfad5b32c055ee14106601cb96e06f'

session_folder = 'session'
session_name = 'autopost'
group_log_id = -1002587161294  # Grup tujuan log

# Baca nomor dari input
phone_number = input("Masukkan nomor telepon (format internasional, ex: +62xxxx): ").strip()

# Baca isi teks dari autopost.txt
with open('autopost.txt', 'r', encoding='utf-8') as f:
    text_to_post = f.read().strip()

# Baca daftar link grup/channel
with open('linkpost.txt', 'r', encoding='utf-8') as f:
    link_list = [line.strip() for line in f if line.strip()]

# Pastikan folder session ada
if not os.path.exists(session_folder):
    os.makedirs(session_folder)

async def main():
    client = TelegramClient(os.path.join(session_folder, session_name), api_id, api_hash)
    await client.start(phone=phone_number)
    await asyncio.sleep(random.uniform(18, 30))  # Delay aman

    log_lines = []
    async with client:
        for i, link in enumerate(link_list, start=1):
            try:
                await client.send_message(link, text_to_post)
                log_lines.append(f"[{i}] ✅ Sukses: {link}")
                print(f"[{i}] ✅ Terkirim : {link}")
            except ChatWriteForbiddenError:
                log_lines.append(f"[{i}] ❌ Not allowed cih {link}")
                print(f"[{i}] ❌ Gak punya izin kirim ke {link}")
            except ChannelPrivateError:
                log_lines.append(f"[{i}] 🚫 Private  {link}")
                print(f"[{i}] 🚫 Channel private / tidak bisa diakses: {link}")
            except FloodWaitError as e:
                log_lines.append(f"[{i}] ⏱️ Spam delay {e.seconds}s")
                print(f"[{i}] ⏱️ Kena spam delay, nunggu {e.seconds}s")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                log_lines.append(f"[{i}] ⚠️ Error cih {link}")
                print(f"[{i}] ⚠️ Error ngirim {link}: {e}")
            await asyncio.sleep(random.uniform(18, 30))  # Delay aman

        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        log_lines.append(f"\n🟢 done cih ({now})")

        log_text = "\n".join(log_lines)
        await asyncio.sleep(random.uniform(18, 30))  # Delay aman

        await client.send_message(group_log_id, f"[📋 Log]\n\n{log_text}")

    print("\n✅ Semua selesai. Log juga dikirim ke grup.")

if __name__ == '__main__':
    asyncio.run(main())
# +6283199369009