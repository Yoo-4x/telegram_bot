from login import tg
from functools import wraps
import time,sched

def sendMessage(chat_id, text):
    tg.send_message(
        chat_id=chat_id,
        text=text,
    )

def sendMessageByName(username, text):
    result = tg.call_method('searchPublicChat', params={'username': username}, block=True)
    chat_id = result.update['id']
    sendMessage(chat_id, text)

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

