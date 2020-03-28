from login import tg
from functools import wraps
from interceptor import interceptor
from retrying import retry
import time,sched 

def sendMessageByName(username, text, reply=0):
    return sendMessage(getUserId(username), text, reply)
def sendMessage(chat_id, text, reply=0):
    return _sendMessage(chat_id, text, 'message', reply)

def sendImageByName(username, text, reply=0):
    return sendImage(getUserId(username), text, reply)
def sendImage(chat_id, text, reply=0):
    return _sendMessage(chat_id, text, 'image', reply)

def sendFileByName(username, text, reply=0):
    return sendFile(getUserId(username), text, reply)
def sendFile(chat_id, text, reply=0):
    return _sendMessage(chat_id, text, 'file', reply)

@retry(wait_exponential_multiplier=100, wait_exponential_max=1000)
def _sendMessage(chat_id, text, mType, reply):
    data = {}
    data['@type'] = 'sendMessage'
    data['chat_id'] = chat_id
    data['reply_to_message_id'] = reply
    if mType == 'message':
        data['input_message_content'] = {
                '@type': 'inputMessageText',
                'text': {'@type': 'formattedText', 'text': text},
                }
    elif mType == 'image':
        data['input_message_content'] = {
                '@type': 'inputMessagePhoto',
                'photo': {'@type': 'inputFileLocal', 'path': text},
                }
    elif mType == 'file':
        data['input_message_content'] = {
                '@type': 'inputMessageDocument',
                'document': {'@type': 'inputFileLocal', 'path': text},
                }
    else:
        data['input_message_content'] = {
                '@type': 'inputMessageText',
                'photo': {'@type': 'formattedText', 'text': '发送文件类型错误'},
                }
    return tg._send_data(data, block=True)

def MessageReadedByName(username, message_id):
    return MessageReaded(getUserId(username), message_id)
@retry(wait_exponential_multiplier=100, wait_exponential_max=1000)
def MessageReaded(chat_id, message_id):
    r = tg.call_method('getChat', params={'chat_id': chat_id}, block=True)
    if r.update['last_read_outbox_message_id'] >= message_id:
        return True
    else:
        return False
@retry(wait_exponential_multiplier=100, wait_exponential_max=1000)
def fileDownload(remote_file_id, priority=2, synchronous=False):
    result = tg.call_method('getRemoteFile', params={'remote_file_id':remote_file_id}, block=True)
    tg.call_method('downloadFile', params={'file_id':result.update['id'], 'priority':priority, 'synchronous':synchronous}, block=True)

@retry(wait_exponential_multiplier=100, wait_exponential_max=1000)
def getUsername(chat_id):
    result = tg.call_method('getUser', params={'user_id': chat_id}, block=True)
    return result.update['username']
@retry(wait_exponential_multiplier=100, wait_exponential_max=1000)
def getUserId(username):
    result = tg.call_method('searchPublicChat', params={'username': username}, block=True)
    return result.update['id']

def listFunctions(chat_id, funs, message_id, text=''):
    for index, key in enumerate(funs.keys()):
        if type(funs[key]) == str:
            text += str(index) + " - " + key + ' ' + funs[key] + '\n'
        else:
            text += str(index) + " - " + key + ' ' + '\n'
    sendMessage(chat_id, text, message_id)


def load(filePath):
    try:
        with open(filePath, 'r') as fp:
            content = []
            for line in fp.readlines():
                line = line.strip('\n')
                content.append(line)
    except IOError:
        with open(filePath, 'w') as fp:
            content = []
    return content
def save(filePath, lines):
    with open(filePath, 'w') as fp:
        fp.writelines([line+'\n' for line in lines])

