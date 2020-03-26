from config import userId
from time import sleep
from functools import wraps
'''
对Tg服务器的消息进行拦截
'''
class interceptor:

    def __isSelf(sender_id):
        return sender_id == userId

    @classmethod
    def MessageInDealing(cls, func):
        # 不响应自己发出的消息
        @wraps(func)
        def wrapper(self, update):
            if not cls.__isSelf(update['message']['sender_user_id']):
                message_content = update['message']['content']
                message_text = message_content.get('text', {}).get('text', '').lower()
                message_type = message_content['@type']
                chat_id = update['message']['chat_id']
                message_id =  update['message']['id']

                func(self, chat_id, message_type, message_text, message_id)
        return wrapper

    @classmethod
    def errorAndRetry(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                sleep(60)
                return wrapper(self, *args, **kwargs)
        return wrapper
