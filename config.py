import os

API_ID = int(os.environ.get("API_ID", 0))  
API_HASH = os.environ.get("API_HASH", "")  
OWNER_ID = [int(i) for i in os.environ.get("OWNER_ID", "0").split()]
SESSION_STRING = os.environ.get("SESSION_STRING", "")
