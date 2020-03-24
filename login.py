from telegram.client import Telegram
from config import api_id, api_hash, phone, database_encryption_key, setting, proxy_server, proxy_port, proxy_type

def login():
    tg = Telegram(
         api_id=api_id,
         api_hash=api_hash,
         phone=phone,
         database_encryption_key=database_encryption_key,
         proxy_server=proxy_server,
         proxy_port=proxy_port,
         proxy_type=proxy_type,
    )
    tg.login()

    return tg

tg = login()
