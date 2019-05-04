import os


PORT_ENV_NAME = 'GLOCKR_PORT'
if PORT_ENV_NAME in os.environ:
    PORT = os.environ[PORT_ENV_NAME]
else:
    PORT = '29410'

CHARSET = 'utf-8'

ROUTER = {
    'heartbeat': '/',
    'add': '/res/add',
    'remove': '/res/remove',
    'show_all': '/res',
    'acquire': '/res/acquire',
    'release': '/res/release',
}
