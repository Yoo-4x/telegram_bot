from interceptor import interceptor
from func import func
import re
import time
import threading
from utils import setChatMemberStatus, sendMessage, getMessage, getUsername
from config import userId, groups



wait = {}
class func_group(func):
    def __slience(self, chat_id):
        time.sleep(10)
        if wait:
            for w in wait.keys():
                setChatMemberStatus(chat_id, w, 'kick')
    
    @interceptor.groupChat
    @interceptor.MessageInDealing
    def func_handler(self, chat_id, message_type, message_text, message_id, user_id):
        if chat_id in groups:
            # 有新人加入
            if  message_type == 'messageChatAddMembers':
                note= '''
Hola,%s
能否做出以下约定：
- 敬党爱国，不发表过激言论
感谢、
请在30s内回复(reply)此信息
(是/否) 
                ''' % getUsername(user_id)

                sendMessage(chat_id, note, user_id=user_id, mention=True)
                wait[str(user_id)] = '是'
                # 线程等待，程序继续运行
                p = threading.Thread(target=self.__slience, args=(chat_id,))
                p.setDaemon(True)
                p.start()
            else:
                ms = getMessage(chat_id, message_id)
                # 消息是否是回复类消息
                if ms['reply_to_message_id'] != 0:
                    new_ms = getMessage(chat_id, ms['reply_to_message_id'])
                    # 消息是回复机器人的消息
                    if new_ms['sender_user_id'] == userId:
                        # 发消息人是否在等待列表
                        if str(user_id) in wait.keys():
                            if re.findall(wait[str(user_id)], message_text)[0]:
                                wait.pop(str(user_id))

