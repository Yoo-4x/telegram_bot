from interceptor import interceptor
from utils import listFunctions, sendMessage
from config import echoFuns
from echo_bot_func import filters, arguExplain
import re

'''
massgae handler:
    func:
        keywords filer:
        {keywords: dealing function}
'''

@interceptor.MessageInDealing
def echo_bot_handler(chat_id, message_type, message_text):

    if  message_type == 'messageText':
        if re.search('^/echo.*', message_text):
            for key, func in echoFuns.items():
                if re.search('/echo.*'+key+'.*', message_text):
                    if key == 'list':
                        eval(func[0])(chat_id=chat_id, funs=eval(func[1]))
                    elif key == 'update':
                        eval(func[0])(chat_id=chat_id, text=eval(func[1]))
                    return 0
            listFunctions(chat_id, echoFuns, '')
        for key, text in filters.items():
            if re.search('^[^/]?.*'+key+'.*', message_text):
                sendMessage(chat_id, text)
                return 0
