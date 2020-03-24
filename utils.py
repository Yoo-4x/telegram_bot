from login import tg
from functools import wraps
import time,sched


def sendMessageByName(username, text):
    chat_id = getUserId(username)
    sendMessage(chat_id, text)
def sendMessage(chat_id, text):
    _sendMessage(chat_id, text, 'message')

def sendImageByName(username, text):
    chat_id = getUserId(username)
    sendImage(chat_id, text)
def sendImage(chat_id, text):
    _sendMessage(chat_id, text, 'image')

def sendFileByName(username, text):
    chat_id = getUserId(username)
    sendFile(chat_id, text)
def sendFile(chat_id, text):
    _sendMessage(chat_id, text, 'file')

def _sendMessage(chat_id, text, mType):
    data = {}
    data['@type'] = 'sendMessage'
    data['chat_id'] = chat_id
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
    r = tg._send_data(data, block=True)

def getUsername(chat_id):
    result = tg.call_method('getUser', params={'user_id': chat_id}, block=True)
    return result.update['username']

def getUserId(username):
    result = tg.call_method('searchPublicChat', params={'username': username}, block=True)
    return result.update['id']

def listFunctions(chat_id, funs, text=''):
    for index, key in enumerate(funs.keys()):
        if type(funs[key]) == str:
            text += str(index) + " - " + key + ':' + funs[key] + '\n'
        else:
            text += str(index) + " - " + key + ':' + '\n'
    sendMessage(chat_id, text)


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

