from func import func
import requests
from bs4 import BeautifulSoup as bs
import threading
import re
import os
import json
import time,sched
import threading
from retrying import retry
from urllib.parse import urlparse
from utils import sendMessageByName, sendMessage, getUsername, load, save
from interceptor import interceptor

class func_novel(func):
    def __init__(self):
        self.file_dir = './novel/'
        self.config = self.file_dir + 'novel.conf'
        self.websit= {
                        'biquge': self.biquge
                     }
        self.webs={
                    '笔趣阁':'biquge'
                  }
        if not os.path.exists(self.file_dir):
            os.makedirs(self.file_dir)

        p=threading.Thread(target=self.deamon)
        # 为使 ctrl+c 能够正常关闭多线程
        p.setDaemon(True)
        p.start()

    @interceptor.MessageInDealing
    def func_handler(self, chat_id, message_type, message_text, message_id):
        self.message_id = message_id
        if  message_type == 'messageText':
            if re.search('^/nov.*', message_text):
                self.arguExplain(chat_id, message_text)

    def deamon(self):
        schedule = sched.scheduler(time.time, time.sleep)
        while True:
            # 10分钟一次
            schedule.enter(600,0, self.main)
            schedule.run()
    def arguExplain(self, chat_id, text):
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
            self.updateConf(chat_id, opt, web, path, index, name)
        except IndexError:
            sendMessage(chat_id, '请求格式：添加|删除|列出,添加{笔趣阁(www.biduo.cc),目录链接,小说名}| 删除{索引}| 列出', self.message_id)
    def updateConf(self, chat_id, option, web, path, index, name):
        conf_str = load(self.config)
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
            sendMessage(chat_id, text, self.message_id)
        else:
            if option == '添加':
                if web in self.webs:
                    web = self.webs[web]
                conf.append({'web': web, 'user': username, 'path': path, 'history': name, 'name': name})
            elif option == '删除':
                conf.pop(index)
            conf.extend(conf_other)

            conf_str = []
            for c in conf:
                conf_str.append(json.dumps(c, ensure_ascii=False))
            save(self.config, conf_str)
            
    def main(self):
        confs = load(self.config)
        if len(confs) == 0:
            exit()
        for conf in confs:
            conf = json.loads(conf)
            self.websit[conf['web']](path=str(urlparse(conf['path'].path)), user=conf['user'], history_path=conf['history'], name=conf['name'])
            #防止请求频率过高
            time.sleep(1)

    @retry(wait_fixed=20000)
    def getContent(self, url):
        req = requests.get(url)

        soup = bs(req.content.decode("gbk"), 'html.parser')
        title = soup.select('h1')[0].get_text()
        content = soup.select('div > #content')[0].get_text()
        content = re.sub('\xa0\xa0\xa0\xa0', '\n', content)
        return title, content
    def biquge(self, path, user, history_path, name):
        base_url = 'https://www.biduo.cc'
        history = load(self.file_dir + history_path)
        new = self.update(base_url, path)
        if len(history) > 0:
            for url in new:
                if url not in history:
                    title, content = self.getContent(url)
                    sendMessageByName(user, name + ':' + title)
                    cuts = len(content)//4000
                    for cut in range(cuts+1):
                        sendMessageByName(user, content[cut * 4000 : (cut+1) * 4000])
        save(self.file_dir + history_path, new)
    @retry(wait_fixed=20000)
    def update(self, base_url, path):
        req = requests.get(base_url + path)
        soup = bs(req.content.decode("gbk"), 'html.parser')
        ret = []
        for tag in soup.select('dd > a')[-5:]:
            ret.append(base_url + tag['href'])
        return ret
