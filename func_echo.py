import re
import json
from utils import sendMessage, listFunctions, load, save
from interceptor import interceptor
from config import echoFuns
from func import func

class func_echo(func):
    def __init__(self):
        self.conf_path='./echo'

        self.filters = {}
        for line in  load(self.conf_path):
            line = json.loads(line)
            self.filters[list(line.keys())[0]] = list(line.values())[0]
    '''
    massgae handler:
        func:
            keywords filer:
            {keywords: dealing function}
    '''

    @interceptor.MessageInDealing
    def func_handler(self, chat_id, message_type, message_text, message_id):
        self.message_id = message_id

        if  message_type == 'messageText':
            if re.search('^/echo.*', message_text):
                for key, func in echoFuns.items():
                    if re.search('/echo.*'+key+'.*', message_text):
                        if key == 'list':
                            eval(func[0])(chat_id=chat_id, funs=eval('self.'+func[1]))
                        elif key == 'update':
                            eval('self.'+func[0])(chat_id=chat_id, text=eval(func[1]))
                        return 0
                listFunctions(chat_id, echoFuns, '')
            for key, text in self.filters.items():
                if re.search('^[^/]?.*'+key+'.*', message_text):
                    sendMessage(chat_id, text, self.message_id)
                    return 0
    '''
    Argu:

        option: add     # add keyword or  filter if index not present
                delete, # delete keyword
                update  # update replay text drop    # delete filter
    '''
    def updateFilter(self, chat_id, option, index, key='', text=''):
        #index, key, text
        index = int(index)
        if option == '添加':
            # 添加新的关键字
            if index < len(self.filters) and index >= 0:
                index_key = list(self.filters.keys())[index]
                self.filters[index_key + '|' + key] = self.filters.pop(index_key)
            # 添加新的规则
            else:
                self.filters[key] = text
        #key
        if option == '删除':
            if key in self.filters.keys():
                del self.filters[key]
        #key, text
        if option == '更新':
            self.filters[key] = text
        #index, key, text
        if option == '去关键词':
            index_key = list(self.filters.keys())[index]
            after_key = re.sub(text, '', index_key)
            after_key = re.sub('\|\|', '', after_key)
            self.filters[after_key] = self.filters.pop(index_key)
        listFunctions(chat_id, self.filters, '更新后：\n')
        save(self.conf_path, [json.dumps(self.filters, ensure_ascii=False)])

    #text -> 指令,option,index,key,text
    def arguExplain(self, chat_id, text):
        text = re.sub('｜', '|', text)
        # 去除空格
        text = re.sub(' ', '', text)
        args = re.split(',|，', text)

        try:
            opt = args[2]
            # 假定 args[2] 是 int，不是捕捉报错再按字符串对待
            try:
                index = int(args[3])
                if index >= len(self.filters.keys()):
                    key = args[4]
                else:
                    key = list(self.filters.keys())[index]
            except ValueError:
                key = args[3]
                if key in self.filters.keys():
                    index = list(self.filters.keys()).index(key)
                else:
                    index = len(self.filters)
            text = args[-1]
            self.updateFilter(chat_id, opt, index=index, key=key, text=text)
        except IndexError:
            sendMessage(chat_id, '请求格式：添加|删除|更新|去关键词,index,key,text', self.message_id)
