import asyncio
import json
import os
from pyrogram import Client, filters, enums
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import FloodWait
# Import styles milik Benxx
from .styles import result_box, status_report, success, error, mono, bold, list_items

# --- KONFIGURASI DATABASE ---
BLACKLIST_FILE = "data/blacklist.json"
if not os.path.exists("data"):
    os.makedirs("data")

def get_blacklist():
    try:
        with open(BLACKLIST_FILE, "r") as f:
            data = json.load(f)
            # Pastikan ID dalam bentuk integer
            return {"groups": [int(i) for i in data.get("groups", [])]}
    except (FileNotFoundError, json.JSONDecodeError):
        return {"groups": []}

def save_blacklist(data):
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- MODULE BLACKLIST & GCAST ---

@Client.on_message(filters.command(["bl", "unbl"], ".") & filters.me)
async def blacklist_logic(client, message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return await message.edit(error("Harus di dalam grup!"))
    
    cmd = message.command[0]
    bl = get_blacklist()
    chat_id = int(message.chat.id)
    chat_title = message.chat.title

    if cmd == "bl":
        if chat_id in bl["groups"]:
            return await message.edit(success(f"Grup {mono(chat_title)} sudah ada di blacklist.", title="ℹ️ SUDAH ADA"))
        bl["groups"].append(chat_id)
        save_blacklist(bl)
        await message.edit(success(f"Grup {mono(chat_title)} berhasil di-blacklist.", title="✅ BLACKLISTED"))
    else:
        if chat_id not in bl["groups"]:
            return await message.edit(error(f"Grup {mono(chat_title)} tidak terdaftar."))
        bl["groups"].remove(chat_id)
        save_blacklist(bl)
        await message.edit(success(f"Grup {mono(chat_title)} dihapus dari blacklist.", title="✅ UNBLACKLISTED"))

@Client.on_message(filters.command("gcast", ".") & filters.me)
async def gcast_improved(client, message):
    msg = message.reply_to_message if message.reply_to_message else None
    
    if not msg and len(message.command) < 2:
        return await message.edit(error("Reply ke pesan atau ketik teks untuk GCAST!"))

    status_msg = await message.edit(bold("📢 Menyiapkan Broadcast..."))
    sent, failed, skipped = 0, 0, 0
    blacklist = get_blacklist()["groups"]

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            chat_id = int(dialog.chat.id)
            if chat_id in blacklist:
                skipped += 1
                continue
            try:
                if msg:
                    await msg.copy(chat_id)
                else:
                    text_to_send = message.text.split(None, 1)[1]
                    await client.send_message(chat_id, text_to_send)
                
                sent += 1
                await asyncio.sleep(0.3) # Jeda aman
            except FloodWait as e:
                await asyncio.sleep(e.value) # Tunggu kalau kena limit
                if msg: await msg.copy(chat_id)
                else: await client.send_message(chat_id, text_to_send)
                sent += 1
            except Exception:
                failed += 1

    await status_msg.edit(
        status_report(sent, failed, total=sent+failed+skipped, process_name="GCAST") + 
        f"\n⏭️ {bold('Di-skip (Blacklist):')} {mono(skipped)}"
    )

# --- MODULE ADMIN ---

@Client.on_message(filters.command("adminlist", ".") & filters.me)
async def adminlist_handler(client, message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return await message.edit(error("Fitur ini hanya untuk Grup!"))
    
    await message.edit(bold("Memuat daftar admin..."))
    admins = []
    owner = ""

    try:
        async for m in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            name = m.user.first_name if not m.user.is_deleted else "Akun Terhapus"
            mention = f"[{name}](tg://user?id={m.user.id})"
            if m.status == ChatMemberStatus.OWNER:
                owner = f"👑 {bold('Owner:')} {mention}\n"
            else:
                admins.append(mention)
        
        res = list_items(admins, title=f"🛡️ ADMIN: {message.chat.title}")
        await message.edit(f"{owner}{res}")
    except Exception as e:
        await message.edit(error(str(e)))
