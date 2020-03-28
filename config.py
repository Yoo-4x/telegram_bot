# user information
api_id=''
api_hash=''
phone=''
database_encryption_key=''
# get by tg.get_me()
userId = 
master = 

# proxy
# proxyTypeHttp or proxyTypeSocks5, proxyTypeMtproto
setting = {'@type': 'proxyTypeHttp'}
setting['username'] = ''
setting['password'] = ''

proxy_server=None
proxy_port= 0
proxy_type=setting

# modules
funs={}
funs['/echo'] = '自动回复'
funs['/nov'] = '小说订阅'

echoFuns={}
echoFuns['list'] = ['listFunctions', 'filters']
echoFuns['update'] = ['arguExplain', 'message_text']

handler=[
        'list_handler',
        'echo_handler',
        'novel_handler'
]

