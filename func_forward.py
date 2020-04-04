from interceptor import interceptor
from func import func
from config import master
from utils import forwardMessage, getMessage, sendMessage

class func_forward(func):

    @interceptor.secretChat
    @interceptor.MessageInDealing
    def forward_handler(self, chat_id, message_type, message_text, message_id, user_id):
        if chat_id != master:
            forwardMessage(master, chat_id, message_id)
        else:
            cur_message = getMessage(chat_id, message_id)
            reply_to = cur_message['reply_to_message_id']
            if reply_to != 0:
                repl_message = getMessage(chat_id, reply_to)
                chat_id_reply = repl_message['forward_info']['origin']['sender_user_id']
                forwardMessage(chat_id_reply, chat_id, message_id, send_copy=True)
