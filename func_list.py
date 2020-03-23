from interceptor import interceptor
from utils import listFunctions
from config import funs
from func import func


class func_list(func):
    @interceptor.MessageInDealing
    def func_handler(self, chat_id, message_type, message_text):

        if  message_type == 'messageText':
            if '/' == message_text:
                listFunctions(chat_id, funs, '')