from login import tg
from interceptor import interceptor
from utils import listFunctions
from config import funs


@interceptor.MessageInDealing
def func_handler(chat_id, message_type, message_text):

    if  message_type == 'messageText':
        if '/' == message_text:
            listFunctions(chat_id, funs, '')
