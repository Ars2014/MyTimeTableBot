# -*- coding:utf-8; -*-

import configparser
import os

config_file = os.path.join(os.path.dirname(__file__), '..', 'config.ini')

if not os.path.exists(config_file):
    raise FileNotFoundError('Please, create config.ini file in a root of the project.')

config = configparser.ConfigParser()
config.read(config_file)

# Bot settings
token = config['BOT']['TOKEN']

# DB settings
db_host = config['DATABASE']['HOST']
db_port = config['DATABASE']['PORT']
db_user = config['DATABASE']['USER']
db_password = config['DATABASE']['PASSWORD']

# Webhook settings
if config.has_section('WEBHOOK'):
    use_webhook = True
    server_port = int(config.get('WEBHOOK', 'SERVER_PORT'))
    webhook_url_path = config.get('WEBHOOK', 'PATH')
    webhook_host = config.get('WEBHOOK', 'HOST')
    webhook_port = int(config.get('WEBHOOK', 'PORT'))
    webhook_listen = config.get('WEBHOOK', 'LISTEN')
    webhook_url_base = 'https://{host}:{port}'.format(host=webhook_host,
                                                      port=webhook_port)
else:
    use_webhook = False
