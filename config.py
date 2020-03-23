# user information
api_id=''
api_hash=''
phone=''
database_encryption_key='changeme1234'
# get by tg.get_me()
userId = ''

# modules
funs={}
funs['/echo'] = '自动回复'
funs['/nov'] = '小说订阅'

echoFuns={}
echoFuns['list'] = ['listFunctions', 'filters']
echoFuns['update'] = ['arguExplain', 'message_text']

handler=[
        'func_handler',
        'echo_bot_handler',
        'novel_handler'
]

