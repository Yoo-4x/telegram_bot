from interceptor import interceptor
from abc import abstractmethod
import threading

class func:
    '''
    每一个功能都分为信息处理函数和后台进程，两者通过文件进行信息交换
    '''
    def __init__(self):
        p=threading.Thread(target=self.deamon)
        # 为使 ctrl+c 能够正常关闭多线程
        p.setDaemon(True)
        p.start()

    '''
    处理收到的信息
    '''
#    @interceptor.MessageInDealing
#    @classmethod
    @abstractmethod
    def func_handler(self, chat_id, message_type, message_text):
        pass
    '''
    后台程序
    '''
    def deamon(self):
        pass
