from interceptor import interceptor
from novel_func import arguExplain
import re

@interceptor.MessageInDealing
def novel_handler(chat_id, message_type, message_text):

    if  message_type == 'messageText':
        #为了避免在迭代过程中不能修改字典的问题
        if re.search('^/nov.*', message_text):
            arguExplain(chat_id, message_text)
