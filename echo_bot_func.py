import re
import json
from utils import sendMessage, listFunctions, load, save

conf_path='./echo'
'''
Argu:

    option: add     # add keyword or  filter if index not present
            delete, # delete keyword
            update  # update replay text drop    # delete filter
'''
def updateFilter(chat_id, option, index, key='', text=''):
    #index, key, text
    index = int(index)
    if option == '添加':
        # 添加新的关键字
        if index < len(filters) and index >= 0:
            index_key = list(filters.keys())[index]
            filters[index_key + '|' + key] = filters.pop(index_key)
        # 添加新的规则
        else:
            filters[key] = text
    #key
    if option == '删除':
        if key in filters.keys():
            del filters[key]
    #key, text
    if option == '更新':
        filters[key] = text
    #index, key, text
    if option == '去关键词':
        index_key = list(filters.keys())[index]
        after_key = re.sub(text, '', index_key)
        after_key = re.sub('\|\|', '', after_key)
        filters[after_key] = filters.pop(index_key)
    listFunctions(chat_id, filters, '更新后：\n')
    save(conf_path, [json.dumps(filters, ensure_ascii=False)])
#text -> 指令,option,index,key,text
def arguExplain(chat_id, text):
    text = re.sub('｜', '|', text)
    # 去除空格
    text = re.sub(' ', '', text)
    args = re.split(',|，', text)

    try:
        opt = args[2]
        # 假定 args[2] 是 int，不是捕捉报错再按字符串对待
        try:
            index = int(args[3])
            if index >= len(filters.keys()):
                key = args[4]
            else:
                key = list(filters.keys())[index]
        except ValueError:
            key = args[3]
            if key in filters.keys():
                index = list(filters.keys()).index(key)
            else:
                index = len(filters)
        text = args[-1]
        updateFilter(chat_id, opt, index=index, key=key, text=text)
    except IndexError:
        sendMessage(chat_id, '请求格式：添加|删除|更新|去关键词,index,key,text')
filters = {}
for line in  load(conf_path):
    line = json.loads(line)
    filters[list(line.keys())[0]] = list(line.values())[0]
