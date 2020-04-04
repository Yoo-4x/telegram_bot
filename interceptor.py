from config import userId, master
from time import sleep
from functools import wraps
'''
对Tg服务器的消息进行拦截
'''
class interceptor:

    def __isSelf(sender_id):
        return sender_id == userId
    def __isMaster(sender_id):
        return sender_id == master
    def __isGroup(chat_id):
        return chat_id < 0

    @classmethod
    def MessageInDealing(cls, func):
        # 不响应自己发出的消息
        @wraps(func)
        def wrapper(self, update):
            user_id = update['message']['sender_user_id']
            if not cls.__isSelf(user_id):
                message_content = update['message']['content']
                message_text = message_content.get('text', {}).get('text', '').lower()
                message_type = message_content['@type']
                chat_id = update['message']['chat_id']
                message_id =  update['message']['id']

                func(self, chat_id, message_type, message_text, message_id, user_id)
        return wrapper
    @classmethod
    def isMaster(cls, func):
        @wraps(func)
        def wrapper(self, update):
            if cls.__isMaster(update['message']['sender_user_id']):
                return func(self, update)
        return wrapper

    @classmethod
    def notMaster(cls, func):
        @wraps(func)
        def wrapper(self, update):
            if cls.__isMaster(update['message']['sender_user_id']):
                return func(self, update)
        return wrapper

    @classmethod
    def secretChat(cls, func):
        @wraps(func)
        def wrapper(self, update):
            if not cls.__isGroup(update['message']['chat_id']):
                return func(self, update)
        return wrapper

    @classmethod
    def groupChat(cls, func):
        @wraps(func)
        def wrapper(self, update):
            if cls.__isGroup(update['message']['chat_id']):
                return func(self, update)
        return wrapper
