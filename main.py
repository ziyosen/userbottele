from app import app
import pyromod
import importlib
import os
import sys
from config import OWNER_ID

print("ðŸš€ Memulai Benxx Userbot...")

# Tambahkan current directory ke sys.path biar import gak nyasar
sys.path.append(os.getcwd())

# Memastikan folder modules terbaca secara manual
if os.path.exists("modules"):
    for file in os.listdir("modules"):
        # Hanya load file .py dan bukan __init__.py atau file sementara
        if file.endswith(".py") and not file.startswith("__"):
            module_name = file[:-3]
            try:
                # Pastikan formatnya modules.nama_file tanpa titik di ujung
                importlib.import_module(f"modules.{module_name}")
                print(f"âœ… Loaded: {module_name}")
            except Exception as e:
                print(f"âŒ Gagal load {module_name}: {e}")
else:
    print("âš ï¸ Folder 'modules' tidak ditemukan!")

if __name__ == "__main__":
    # Cek apakah OWNER_ID sudah terisi
    if not OWNER_ID:
        print("âš ï¸ PERINGATAN: OWNER_ID masih kosong di config.py!")
    else:
        print(f"ðŸ‘‘ Owner ID Terdeteksi: {OWNER_ID}")

    print("ðŸ”¥ Benxx Userbot is Online!")
    try:
        app.run()
    except Exception as e:
        print(f"ðŸš« Bot Berhenti: {e}")
