# modules/keepalive.py
import asyncio
from app import app
from pyrogram import filters
from pyrogram.types import Message
from .styles import result_box, bold, mono

# ========== KEEP ALIVE TASK ==========

async def keep_alive_task():
    """Looping untuk menjaga koneksi tetap hidup."""
    while True:
        try:
            # 1. Lakukan ping ke API Telegram (aktivitas ringan)
            await app.get_me()
            
            # 2. Kirim pesan ke Saved Messages (opsional, biar keliatan ada log)
            await app.send_message(
                "me",
                f"🛰️ Keep Alive: {asyncio.get_event_loop().time()}"
            )
            
            # 3. Tunggu 20 menit (1200 detik)
            #    Jangan 30 menit karena bisa timeout di beberapa jaringan
            await asyncio.sleep(1200)
            
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"[KeepAlive] Error: {e}")
            await asyncio.sleep(30)  # tunggu sebentar lalu coba lagi

# ========== PERINTAH MANUAL ==========

@app.on_message(filters.command("ping", ".") & filters.me)
async def ping_command(client, message: Message):
    """Cek apakah bot masih hidup."""
    start = asyncio.get_event_loop().time()
    await app.get_me()  # test koneksi
    latency = (asyncio.get_event_loop().time() - start) * 1000
    await message.edit(
        result_box(
            "🏓 PONG!",
            f"✅ {bold('Status:')} Connected\n"
            f"⚡ {bold('Latency:')} `{latency:.0f}ms`\n"
            f"🕐 {bold('Server Time:')} `{asyncio.get_event_loop().time():.0f}`",
            icon="🚀"
        )
    )

@app.on_message(filters.command("status", ".") & filters.me)
async def status_command(client, message: Message):
    """Cek status userbot."""
    try:
        me = await app.get_me()
        await message.edit(
            result_box(
                "🤖 BOT STATUS",
                f"✅ {bold('Userbot:')} Aktif\n"
                f"👤 {bold('Akun:')} {me.first_name}\n"
                f"🔋 {bold('Mode:')} Nonstop 24 Jam\n"
                f"🛰️ {bold('KeepAlive:')} Running",
                icon="🔥"
            )
        )
    except Exception as e:
        await message.edit(
            result_box(
                "⚠️ ERROR",
                f"❌ {bold('Status:')} Offline\n"
                f"📝 {bold('Error:')} `{e}`",
                icon="💀"
            )
        )

# ========== START TASK DI BACKGROUND ==========

# Cara yang benar untuk memulai task asyncio di background
# Pyrogram akan menjalankan event loop, kita hanya perlu create task
async def start_keep_alive():
    asyncio.create_task(keep_alive_task())

# Register task agar berjalan saat bot mulai
loop = asyncio.get_event_loop()
if loop.is_running():
    loop.create_task(keep_alive_task())
else:
    # Jika loop belum running, daftarkan untuk nanti
    asyncio.ensure_future(keep_alive_task())
