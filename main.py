from app import app
import pyromod
import importlib
import os
import sys

from config import OWNER_ID

print("🚀 Memulai Userbot...")

# Tambahkan current directory ke sys.path biar import gak nyasar
sys.path.append(os.getcwd())

# Memastikan folder modules terbaca secara manual
if os.path.exists("modules"):
    for file in os.listdir("modules"):
        
        if file.endswith(".py") and not file.startswith("__"):
            module_name = file[:-3]
            try:
                
                importlib.import_module(f"modules.{module_name}")
                print(f"✅ Loaded: {module_name}")
            except Exception as e:
                print(f"❌ Gagal load {module_name}: {e}")
else:
    print("⚠️ Folder 'modules' tidak ditemukan!")

if __name__ == "__main__":
    
    if not OWNER_ID or OWNER_ID == [0]:
        print("⚠️ PERINGATAN: OWNER_ID masih kosong! Cek config.py atau GitHub Secrets.")
    else:
        print(f"👑 Owner ID Terdeteksi: {OWNER_ID}")

    print("🔥 Benxx Userbot is Online!")
    try:
        
        app.run()
    except Exception as e:
        print(f"🚫 Bot Berhenti: {e}")
