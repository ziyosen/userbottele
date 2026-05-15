import pyromod 
from pyrogram import Client
from config import API_ID, API_HASH, SESSION_STRING

app = Client(
    "benxx_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    workers=20
)
