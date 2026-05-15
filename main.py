from app import app
import pyromod
import importlib
import os
import sys
from config import OWNER_ID

print("🚀 Memulai Userbot...")


sys.path.append(os.getcwd())


if os.path.exists("modules"):

    files = sorted(os.listdir("modules"))
    for file in files:

        if file.endswith(".py") and not file.startswith("__"):
            module_name = file[:-3]
            try:
                # Import module secara dinamis
                importlib.import_module(f"modules.{module_name}")
                print(f"✅ Loaded: {module_name}")
            except Exception as e:
                
                print(f"❌ Gagal load {module_name}: {e}")
                continue 
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
