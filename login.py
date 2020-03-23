from telegram.client import Telegram
from config import api_id, api_hash, phone, database_encryption_key

def login():
    tg = Telegram(
         api_id=api_id,
         api_hash=api_hash,
         phone=phone,
         database_encryption_key=database_encryption_key,
    )
    tg.login()

    return tg

tg = login()
