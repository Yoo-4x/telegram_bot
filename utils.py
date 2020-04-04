from login import tg
from functools import wraps
from interceptor import interceptor
from retrying import retry
import time,sched 

def sendMessageByName(username, text, reply=0, user_id=0, mention=False):
    return sendMessage(getUserId(username), text, reply, user_id=user_id, mention=mention)
def sendMessage(chat_id, text, reply=0, user_id=0, mention=False):
    return _sendMessage(chat_id=chat_id, text=text, mType='message', reply=reply, user_id=user_id, mention=mention)

def sendImageByName(username, text, reply=0):
    return sendImage(getUserId(username), text, reply)
def sendImage(chat_id, text, reply=0):
    return _sendMessage(chat_id, text, 'image', reply)

def sendFileByName(username, text, reply=0):
    return sendFile(getUserId(username), text, reply)
def sendFile(chat_id, text, reply=0):
    return _sendMessage(chat_id, text, 'file', reply)

@retry(wait_exponential_multiplier=100, wait_exponential_max=1000)
def _sendMessage(chat_id, text, mType, reply, user_id=0, mention=False):
    data = {}
    data['@type'] = 'sendMessage'
    data['chat_id'] = chat_id
    data['reply_to_message_id'] = reply
    if mType == 'message':
        data['input_message_content'] = {
                '@type': 'inputMessageText',
                'text': {'@type': 'formattedText', 'text': text},
                }
        if mention:
            #data['input_message_content']['text']['text']= '@at \n'+data['input_message_content']['text']['text']
            data['input_message_content']['text'].update({'entities':[{'@type':'textEntity', 'offset': 0, 'length': len(getUsername(user_id))+6, 'type': {'@type': 'textEntityTypeMentionName', 'user_id': user_id}}]})
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

@retry(wait_exponential_multiplier=100, wait_exponential_max=1000)
def forwardMessage(chatId, chatId_from, message_id, send_copy=False):
    result = tg.call_method('forwardMessages', params={'chat_id':chatId, 'from_chat_id':chatId_from, 'message_ids': [message_id], 'send_copy': send_copy}, block=True)
    return result.update

@retry(wait_exponential_multiplier=100, wait_exponential_max=1000)
def getMessage(chat_id, message_id):
    result = tg.call_method('getMessage', params={'chat_id': chat_id, 'message_id': message_id}, block=True)
    return result.update

def setChatMemberStatusByName(chat_id, username, opt):
    setChatMemberStatus(chat_id, getUserId(username), opt)
def setChatMemberStatus(chat_id, user_id, opt):
    if opt == 'admin':
        # 管理员
        status = {'@type': 'chatMemberStatusAdministrator', 'can_change_info': True, 'can_delete_messages': True, 'can_invite_users': True, 'can_restrict_member': True, 'can_pin_messages': True}
    elif opt == 'ban':
        # 封禁
        status = {'@type': 'chatMemberStatusBanned'}
    elif opt == 'kick':
        # 踢出群/解除封禁
        opt = 'chatMemberStatusLeft'
        status = {'@type': 'chatMemberStatusLeft'}
    elif opt == 're':
        # 恢复普通身份
        status = {'@type': 'chatMemberStatusMember'}
    elif opt == 'no':
        status = {'@type': 'chatMemberStatusRestricted', 'is_member': True, 'permissions':{'@type': 'chatPermissions'}}
        opt = 'chatMemberStatusRestricted'
    return tg.call_method('setChatMemberStatus', params={'chat_id': chat_id, 'user_id': user_id, 'status': status})
        

def listFunctions(chat_id, funs, text='', message_id=0):
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

