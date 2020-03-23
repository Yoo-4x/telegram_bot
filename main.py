from login import tg
from config import handler
from func_handler import func_handler
from echo_bot_handler import echo_bot_handler
from novel_handler import novel_handler

for h in handler:
    tg.add_message_handler(eval(h))
print('Done...\n')
tg.idle()
