from login import tg
from config import handler
from func_list import func_list
from func_echo import func_echo
from func_novel import func_novel

list_handler = func_list().func_handler
echo_handler = func_echo().func_handler
novel_handler = func_novel().func_handler

for h in handler:
    tg.add_message_handler(eval(h))
print('Done...\n')
tg.idle()
