from urllib import request
from bs4 import BeautifulSoup as bs
import re
import os
import json
import time,sched
import threading
from urllib.parse import urlparse
from utils import sendMessageByName, sendMessage, getUsername, load, save

file_dir = './novel/'
config = 'novel.conf'

if not os.path.exists(file_dir):
    os.makedirs(file_dir)

def update(base_url, path):
    response = request.urlopen(base_url + path)
    html = response.read()
    html = html.decode("gbk")

    soup = bs(html, 'html.parser')
    ret = []
    for tag in soup.select('dd > a')[-5:]:
        ret.append(base_url + tag['href'])
    return ret

def getContent(url):
    response = request.urlopen(url)
    html = response.read()
    html = html.decode("gbk")

    soup = bs(html, 'html.parser')
    title = soup.select('h1')[0].get_text()
    content = soup.select('div > #content')[0].get_text()
    content = re.sub('\xa0\xa0\xa0\xa0', '\n', content)
    return title, content
def biquge(path, user, history_path, name):
    base_url = 'https://www.biduo.cc'
    history = load(file_dir + history_path)
    new = update(base_url, path)
    if len(history) > 0:
        for url in new:
            if url not in history:
                title, content = getContent(url)
                sendMessageByName(user, name + ':' + title)
                cuts = len(content)//4000
                for cut in range(cuts+1):
                    sendMessageByName(user, content[cut * 4000 : (cut+1) * 4000])
    save(file_dir + history_path, new)

websit= {
        'biquge': biquge
        }
webs={
        '笔趣阁':'biquge'
}

def main():
    confs = load(file_dir + config)
    if len(confs) == 0:
        exit()
    for conf in confs:
        conf = json.loads(conf)
        websit[conf['web']](path=urlparse(conf['path']).path+'/', user=conf['user'], history_path=conf['history'], name=conf['name'])
        #防止请求频率过高
        time.sleep(1)

# 定时执行
def timer():
    schedule = sched.scheduler(time.time, time.sleep)
    while True:
        # 10分钟一次
        schedule.enter(600,0,main)
        schedule.run()
# 线程运行
def deamon():
    p=threading.Thread(target=timer)
    p.setDaemon(True)
    p.start()

# 加载文件时直接运行
deamon()
#text -> 指令,web,conf,user,history_path,name
def updateConf(chat_id, option, web, path, index, name):
    conf_str = load(file_dir + config)
    conf_json=[]
    for c in conf_str:
        conf_json.append(json.loads(c))
    username = getUsername(chat_id)

    conf = [i for i in conf_json if i['user'] == username]
    conf_other = [i for i in conf_json if i['user'] != username]
    if option == '列出':
        text = ''
        for index, c in enumerate(conf):
            text += str(index) + " - " + c['name'] + '\n'
        sendMessage(chat_id, text)
    else:
        if option == '添加':
            if web in webs:
                web = webs[web]
            conf.append({'web': web, 'user': username, 'path': path, 'history': name, 'name': name})
        elif option == '删除':
            conf.pop(index)
        conf.extend(conf_other)

        conf_str = []
        for c in conf:
            conf_str.append(json.dumps(c, ensure_ascii=False))
        save(file_dir + config, conf_str)
        main()

def arguExplain(chat_id, text):
    text = re.sub(' ', '', text)
    args = re.split(',|，', text)
    web=''
    path=''
    index=0
    name=''
    try:
        opt = args[1]
        # 添加｜删除
        if len(args) > 2:
            # 假定 args[2] 是 int，不是捕捉报错再按字符串对待
            # 删除
            try:
                index = int(args[2])
            #添加
            except ValueError:
                web = args[2]
                path = args[3]
                name = args[4]
        updateConf(chat_id, opt, web, path, index, name)
    except IndexError:
        sendMessage(chat_id, '请求格式：添加|删除|列出,添加{笔趣阁(www.biduo.cc),目录链接,小说名}| 删除{索引}| 列出')
