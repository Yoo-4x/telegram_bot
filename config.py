# user information
api_id='1292929'
api_hash='09633fa73f19c403cf46190d632e219c'
phone='+8613258313072'
database_encryption_key='changeme1234'
# get by tg.get_me()
userId = 1096857502

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

